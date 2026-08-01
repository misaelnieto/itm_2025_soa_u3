package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"

	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
)

type registerForm struct {
	inputs    []textinput.Model
	focused   int
	submitted bool
	err       error
}

func newRegisterForm() registerForm {
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
			t.Placeholder = "Correo"
		case 4:
			t.Placeholder = "Habitación"
		}
		inputs[i] = t
	}

	return registerForm{
		inputs:  inputs,
		focused: 0,
	}
}

func (f registerForm) Update(msg tea.Msg) (registerForm, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "tab", "shift+tab", "up", "down":
			f.nextInput()
		case "enter":
			if f.focused == len(f.inputs)-1 {
				return f, f.submit
			}
			f.nextInput()
		}
	}

	var cmd tea.Cmd
	f.inputs[f.focused], cmd = f.inputs[f.focused].Update(msg)
	return f, cmd
}

func (f *registerForm) nextInput() {
	f.focused = (f.focused + 1) % len(f.inputs)
	for i := range f.inputs {
		if i == f.focused {
			f.inputs[i].Focus()
		} else {
			f.inputs[i].Blur()
		}
	}
}

func (f registerForm) View() string {
	if f.submitted {
		return "¡Cliente registrado exitosamente!\nPresiona 'esc' para volver al menú."
	}

	var s strings.Builder
	s.WriteString("=== Registro de Cliente ===\n\n")

	for i := range f.inputs {
		s.WriteString(f.inputs[i].View())
		s.WriteString("\n")
	}

	if f.err != nil {
		s.WriteString(fmt.Sprintf("\nError: %v\n", f.err))
	}

	s.WriteString("\nPresiona Tab para navegar • Enter para enviar • Esc para volver\n")
	return s.String()
}

func (f registerForm) submit() tea.Msg {
	client := map[string]interface{}{
		"first_name":  f.inputs[0].Value(),
		"middle_name": f.inputs[1].Value(),
		"last_name":   f.inputs[2].Value(),
		"email":       f.inputs[3].Value(),
		"room":        f.inputs[4].Value(),
	}

	jsonData, err := json.Marshal(client)
	if err != nil {
		return errMsg(fmt.Errorf("error al preparar datos: %v", err))
	}

	resp, err := http.Post(
		"http://localhost:8000/api/v1/imoreno/hotel/operations/add",
		"application/json",
		bytes.NewBuffer(jsonData),
	)
	if err != nil {
		return errMsg(fmt.Errorf("error al enviar datos: %v", err))
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusCreated {
		return errMsg(fmt.Errorf("error del servidor: %d", resp.StatusCode))
	}

	f.submitted = true
	return nil
}

type errMsg error
