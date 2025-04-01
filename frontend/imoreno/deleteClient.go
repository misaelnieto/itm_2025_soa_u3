package main

import (
	"fmt"
	"net/http"
	"net/url"
	"strings"

	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
)

type deleteForm struct {
	inputs    []textinput.Model
	focused   int
	submitted bool
	err       error
	success   bool
}

func newDeleteForm() deleteForm {
	inputs := make([]textinput.Model, 3)

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
		}
		t.CharLimit = 32
		inputs[i] = t
	}

	return deleteForm{
		inputs:  inputs,
		focused: 0,
	}
}

func (f deleteForm) Update(msg tea.Msg) (deleteForm, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "tab", "shift+tab", "up", "down":
			f.nextInput()
			return f, nil
		case "enter":
			// Validar que al menos un campo esté completo
			if f.inputs[0].Value() == "" && f.inputs[1].Value() == "" && f.inputs[2].Value() == "" {
				f.err = fmt.Errorf("debe ingresar al menos un criterio de búsqueda")
				return f, nil
			}
			return f, f.submit
		}
	case deleteResultMsg:
		f.err = msg.err
		f.success = msg.err == nil
		f.submitted = true
	}

	var cmd tea.Cmd
	f.inputs[f.focused], cmd = f.inputs[f.focused].Update(msg)
	return f, cmd
}

func (f *deleteForm) nextInput() {
	f.focused = (f.focused + 1) % len(f.inputs)
	for i := range f.inputs {
		if i == f.focused {
			f.inputs[i].Focus()
		} else {
			f.inputs[i].Blur()
		}
	}
}

func (f deleteForm) View() string {
	var s strings.Builder
	s.WriteString("=== Eliminación de Cliente ===\n\n")

	for i := range f.inputs {
		s.WriteString(f.inputs[i].View())
		s.WriteString("\n")
	}

	if f.submitted {
		if f.err != nil {
			s.WriteString("\n" + errorStyle.Render(fmt.Sprintf("Error: %v\n", f.err)))
		} else {
			s.WriteString("\n" + successStyle.Render("¡Cliente eliminado exitosamente!\n"))
		}
	}

	s.WriteString("\nPresiona Tab para navegar • Enter para eliminar • Esc para volver\n")
	return s.String()
}

type deleteResultMsg struct {
	err error
}

func (f deleteForm) submit() tea.Msg {
	params := url.Values{}
	if f.inputs[0].Value() != "" {
		params.Add("first_name", f.inputs[0].Value())
	}
	if f.inputs[1].Value() != "" {
		params.Add("middle_name", f.inputs[1].Value())
	}
	if f.inputs[2].Value() != "" {
		params.Add("last_name", f.inputs[2].Value())
	}

	url := fmt.Sprintf("http://localhost:8000/api/v1/imoreno/hotel/operations/delete?%s", params.Encode())
	req, err := http.NewRequest("DELETE", url, nil)
	if err != nil {
		return deleteResultMsg{fmt.Errorf("error al crear la petición: %v", err)}
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return deleteResultMsg{fmt.Errorf("error al enviar la petición: %v", err)}
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusOK {
		return deleteResultMsg{nil}
	} else {
		return deleteResultMsg{fmt.Errorf("error del servidor: %d", resp.StatusCode)}
	}
}

func (f deleteForm) Init() tea.Cmd {
	return nil
}
