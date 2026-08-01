package main

import (
	"fmt"
	"os"
	"strings"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

type model struct {
	cursor     int
	choice     string
	submenu    bool
	form       registerForm
	searchForm searchForm
	updateForm updateForm
	deleteForm deleteForm
}

var menuItems = []string{
	"Registrar Cliente",
	"Buscar Clientes",
	"Actualizar Clientes",
	"Eliminar Clientes",
}

var titleStyle = lipgloss.NewStyle().
	Bold(true).
	Foreground(lipgloss.Color("#FF69B4")).
	Padding(0, 1)

var selectedItemStyle = lipgloss.NewStyle().
	Foreground(lipgloss.Color("#00FF00")).
	Bold(true)

func main() {
	p := tea.NewProgram(model{})
	if _, err := p.Run(); err != nil {
		fmt.Println("Error al iniciar el programa:", err)
		os.Exit(1)
	}
}

func (m model) Init() tea.Cmd {
	return nil
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "esc":
			if m.submenu {
				m.submenu = false
				switch m.choice {
				case "Registrar Cliente":
					m.form = newRegisterForm()
				case "Buscar Clientes":
					m.searchForm = newSearchForm()
				case "Actualizar Clientes":
					m.updateForm = newUpdateForm()
				case "Eliminar Clientes":
					m.deleteForm = newDeleteForm()
				}
			} else {
				return m, tea.Quit
			}
		case "enter":
			if !m.submenu {
				m.choice = menuItems[m.cursor]
				m.submenu = true
				switch m.choice {
				case "Registrar Cliente":
					m.form = newRegisterForm()
				case "Buscar Clientes":
					m.searchForm = newSearchForm()
				case "Actualizar Clientes":
					m.updateForm = newUpdateForm()
				case "Eliminar Clientes":
					m.deleteForm = newDeleteForm()
				}
			}
		case "up":
			if !m.submenu {
				if m.cursor > 0 {
					m.cursor--
				}
			}
		case "down":
			if !m.submenu {
				if m.cursor < len(menuItems)-1 {
					m.cursor++
				}
			}
		}
	}

	if m.submenu {
		switch m.choice {
		case "Registrar Cliente":
			var cmd tea.Cmd
			m.form, cmd = m.form.Update(msg)
			return m, cmd
		case "Buscar Clientes":
			var cmd tea.Cmd
			m.searchForm, cmd = m.searchForm.Update(msg)
			return m, cmd
		case "Actualizar Clientes":
			var cmd tea.Cmd
			m.updateForm, cmd = m.updateForm.Update(msg)
			return m, cmd
		case "Eliminar Clientes":
			var cmd tea.Cmd
			m.deleteForm, cmd = m.deleteForm.Update(msg)
			return m, cmd
		}
	}

	return m, nil
}

func (m model) View() string {
	var view strings.Builder

	title := titleStyle.Render("=== Menú de Gestión de Clientes ===")
	view.WriteString(fmt.Sprintf("%s\n\n", title))

	if m.submenu {
		switch m.choice {
		case "Registrar Cliente":
			return m.form.View()
		case "Buscar Clientes":
			return m.searchForm.View()
		case "Actualizar Clientes":
			return m.updateForm.View()
		case "Eliminar Clientes":
			return m.deleteForm.View()
		default:
			view.WriteString(fmt.Sprintf("Has seleccionado: %s\n", m.choice))
			view.WriteString("Presiona 'esc' para volver al menú principal.\n")
		}
		return view.String()
	}

	for i, item := range menuItems {
		cursor := " "
		style := lipgloss.NewStyle()
		if m.cursor == i {
			cursor = ">"
			style = selectedItemStyle
		}
		view.WriteString(fmt.Sprintf("%s %s\n", cursor, style.Render(item)))
	}
	view.WriteString("\nUsa las teclas de dirección para moverte y 'Enter' para seleccionar.\n")

	return view.String()
}
