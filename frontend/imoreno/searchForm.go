package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"strings"

	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

var errorStyle = lipgloss.NewStyle().Foreground(lipgloss.Color("red"))

type Client struct {
	FirstName  string `json:"first_name"`
	MiddleName string `json:"middle_name"`
	LastName   string `json:"last_name"`
	Email      string `json:"email"`
	Room       int    `json:"room"`
}

type searchForm struct {
	inputs    []textinput.Model
	focused   int
	submitted bool
	err       error
	client    *Client
}

func newSearchForm() searchForm {
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

	return searchForm{
		inputs:  inputs,
		focused: 0,
	}
}

func (f searchForm) Update(msg tea.Msg) (searchForm, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "tab", "shift+tab", "up", "down":
			f.nextInput()
		case "enter":
			// Check that at least one input has data
			hasInput := false
			for _, input := range f.inputs {
				if input.Value() != "" {
					hasInput = true
					break
				}
			}
			if hasInput {
				return f, f.submit
			}
			// No data, show error
			f.err = fmt.Errorf("Ingrese al menos un criterio de búsqueda")
			return f, nil
		}
	case searchResultMsg:
		f.client = msg.client
		f.err = msg.err
		f.submitted = true
	}

	var cmd tea.Cmd
	f.inputs[f.focused], cmd = f.inputs[f.focused].Update(msg)
	return f, cmd
}

func (f *searchForm) nextInput() {
	f.focused = (f.focused + 1) % len(f.inputs)
	for i := range f.inputs {
		if i == f.focused {
			f.inputs[i].Focus()
		} else {
			f.inputs[i].Blur()
		}
	}
}

func (f searchForm) View() string {
	var s strings.Builder
	s.WriteString("=== Búsqueda de Cliente ===\n\n")

	for i := range f.inputs {
		s.WriteString(f.inputs[i].View())
		s.WriteString("\n")
	}

	if f.submitted {
		s.WriteString("\nResultado de la búsqueda:\n")
		if f.err != nil {
			s.WriteString(errorStyle.Render(fmt.Sprintf("Error: %v\n", f.err)))
		} else if f.client != nil {
			s.WriteString(fmt.Sprintf("\nCliente encontrado:\n"))
			s.WriteString(fmt.Sprintf("Nombre: %s\n", f.client.FirstName))
			s.WriteString(fmt.Sprintf("Primer Apellido: %s\n", f.client.MiddleName))
			s.WriteString(fmt.Sprintf("Segundo Apellido: %s\n", f.client.LastName))
			s.WriteString(fmt.Sprintf("Correo Electrónico: %s\n", f.client.Email))
			s.WriteString(fmt.Sprintf("Habitación: %d\n", f.client.Room))
		} else {
			s.WriteString("No se encontró el cliente.\n")
		}
	}

	s.WriteString("\nPresiona Tab para navegar • Enter para buscar • Esc para volver\n")
	return s.String()
}

type searchResultMsg struct {
	client *Client
	err    error
}

func (f searchForm) submit() tea.Msg {
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

	url := fmt.Sprintf("http://localhost:8000/api/v1/imoreno/hotel/operations/search?%s", params.Encode())
	resp, err := http.Get(url)
	if err != nil {
		return searchResultMsg{nil, fmt.Errorf("error al realizar la búsqueda: %v", err)}
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusNotFound {
		return searchResultMsg{nil, nil}
	}

	if resp.StatusCode != http.StatusOK {
		return searchResultMsg{nil, fmt.Errorf("error del servidor: %d", resp.StatusCode)}
	}

	var result struct {
		Data *Client `json:"data"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return searchResultMsg{nil, fmt.Errorf("error al procesar la respuesta: %v", err)}
	}

	return searchResultMsg{result.Data, nil}
}
