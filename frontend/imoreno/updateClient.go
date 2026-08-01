package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"

	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

var successStyle = lipgloss.NewStyle().Foreground(lipgloss.Color("42"))

type updateForm struct {
	inputs    []textinput.Model
	focused   int
	submitted bool
	err       error
	success   bool
	phase     clientUpdatePhase
	client    *Client
}

type clientUpdatePhase int

const (
	searchPhase clientUpdatePhase = iota
	updatePhase
)

func newUpdateForm() updateForm {
	inputs := make([]textinput.Model, 5)

	for i := range inputs {
		t := textinput.New()
		switch i {
		case 0:
			t.Placeholder = "Nombre"
			t.Focus()
		case 1:
			t.Placeholder = "Primer Apellido"
		case 2:
			t.Placeholder = "Segundo Apellido"
		case 3:
			t.Placeholder = "Nuevo Correo"
		case 4:
			t.Placeholder = "Nueva Habitación"
		}
		t.CharLimit = 32
		inputs[i] = t
	}

	return updateForm{
		inputs:  inputs,
		focused: 0,
		phase:   searchPhase,
	}
}

func (f updateForm) Update(msg tea.Msg) (updateForm, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "tab", "shift+tab", "up", "down":
			f.nextInput()
			return f, nil // Importante: retornar nil aquí
		case "enter":
			if f.phase == searchPhase {
				return f, f.search // Importante: retornar el comando
			} else if f.phase == updatePhase {
				return f, f.update // Importante: retornar el comando
			}
		}
	case searchResultMsg:
		if msg.err != nil {
			f.err = msg.err
			return f, nil
		}
		f.client = msg.client
		if f.client != nil {
			f.phase = updatePhase
			// Pre-llenar campos de actualización
			f.inputs[3].SetValue(f.client.Email)
			f.inputs[4].SetValue(fmt.Sprintf("%d", f.client.Room))
		}
		return f, nil
	case updateResultMsg:
		f.err = msg.err
		f.success = msg.err == nil
		f.submitted = true
		return f, nil
	}

	var cmd tea.Cmd
	f.inputs[f.focused], cmd = f.inputs[f.focused].Update(msg)
	return f, cmd
}

func (f *updateForm) nextInput() {
	maxFields := 3
	if f.phase == updatePhase {
		maxFields = 5
	}
	f.focused = (f.focused + 1) % maxFields
	for i := 0; i < maxFields; i++ {
		if i == f.focused {
			f.inputs[i].Focus()
		} else {
			f.inputs[i].Blur()
		}
	}
}

func (f updateForm) View() string {
	var s strings.Builder
	s.WriteString("=== Actualización de Cliente ===\n\n")

	if f.phase == searchPhase {
		s.WriteString("Fase 1: Búsqueda del cliente\n\n")
		for i := 0; i < 3; i++ {
			s.WriteString(f.inputs[i].View())
			s.WriteString("\n")
		}
	} else {
		s.WriteString("Fase 2: Actualización de datos\n\n")
		s.WriteString(fmt.Sprintf("Cliente encontrado: %s %s %s\n\n",
			f.client.FirstName, f.client.MiddleName, f.client.LastName))
		for i := 3; i < 5; i++ {
			s.WriteString(f.inputs[i].View())
			s.WriteString("\n")
		}
	}

	if f.err != nil {
		s.WriteString("\n" + errorStyle.Render(fmt.Sprintf("Error: %v\n", f.err)))
	}

	if f.submitted && f.success {
		s.WriteString("\n" + successStyle.Render("¡Cliente actualizado exitosamente!\n"))
	}

	s.WriteString("\nPresiona Tab para navegar • Enter para continuar • Esc para volver\n")
	return s.String()
}

type updateResultMsg struct {
	err error
}

func (f updateForm) search() tea.Msg {
	// Similar a la búsqueda en searchForm
	// ...código de búsqueda existente...
	return searchResultMsg{nil, nil}
}

func (f updateForm) update() tea.Msg {
	if f.client == nil {
		return updateResultMsg{fmt.Errorf("no se ha encontrado un cliente para actualizar")}
	}

	updateData := map[string]interface{}{
		"first_name":  f.client.FirstName,
		"middle_name": f.client.MiddleName,
		"last_name":   f.client.LastName,
		"email":       f.inputs[3].Value(),
		"room":        f.inputs[4].Value(),
	}

	jsonData, err := json.Marshal(updateData)
	if err != nil {
		return updateResultMsg{fmt.Errorf("error al preparar datos: %v", err)}
	}

	url := "http://localhost:8000/api/v1/imoreno/hotel/operations/update"
	req, err := http.NewRequest("PUT", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return updateResultMsg{fmt.Errorf("error al crear la petición: %v", err)}
	}
	req.Header.Set("Content-Type", "application/json")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return updateResultMsg{fmt.Errorf("error al enviar la petición: %v", err)}
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return updateResultMsg{fmt.Errorf("error del servidor: %d", resp.StatusCode)}
	}

	return updateResultMsg{nil}
}
