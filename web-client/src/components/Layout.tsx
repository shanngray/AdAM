import React, { useContext, useState, useRef, useEffect } from 'react'
import { SecondaryWindowContext } from './SecondaryWindowContext'

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { toggleSecondaryWindow } = useContext(SecondaryWindowContext)
  const [theme, setTheme] = useState('mytheme')
  const [isThemeMenuOpen, setIsThemeMenuOpen] = useState(false)
  const themeMenuRef = useRef<HTMLLIElement>(null)

  const handleThemeChange = (newTheme: string) => {
    setTheme(newTheme)
    document.documentElement.setAttribute('data-theme', newTheme)
    setIsThemeMenuOpen(false)
  }

  const handleResetConversations = () => {
    const ws = new WebSocket("ws://localhost:8080/server/ws")
    ws.onopen = () => {
      ws.send(JSON.stringify({ type: 'reset_conversations' }))
      ws.close()
    }
  }

  const handleClickOutside = (event: MouseEvent) => {
    if (themeMenuRef.current && !themeMenuRef.current.contains(event.target as Node)) {
      setIsThemeMenuOpen(false)
    }
  }

  useEffect(() => {
    if (isThemeMenuOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    } else {
      document.removeEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isThemeMenuOpen])

  const handleThemeMenuToggle = () => {
    setIsThemeMenuOpen(prev => !prev)
  }

  return (
    <div className="flex flex-col h-screen bg-base-200" data-theme={theme}>
      <header className="flex-none h-[7vh] navbar bg-base-100">
        <div className="flex-1">
          <a className="btn btn-ghost normal-case text-xl">Ad.A.M</a>
        </div>
        {/* Dropdown Menu */}
        <div className="dropdown dropdown-end z-50">
          <label tabIndex={0} className="btn m-1">
            Menu
          </label>
          <ul
            tabIndex={0}
            className="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52"
          >
            <li>
              <button onClick={toggleSecondaryWindow}>Secondary Window</button>
            </li>
            <li ref={themeMenuRef} className="relative">
              <button 
                onClick={handleThemeMenuToggle}
                aria-haspopup="true"
                aria-expanded={isThemeMenuOpen}
                className="justify-between w-full"
              >
                Choose Theme
                <svg
                  className="fill-current transform rotate-90"
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                >
                  <path d="M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z" />
                </svg>
              </button>
              {isThemeMenuOpen && (
                <ul
                  className="p-2 bg-base-200 left-half top-0 mt-0 shadow rounded w-40"
                  role="menu"
                >
                  {['light', 'dark', 'cupcake', 'lemonade', 'mytheme'].map((t) => (
                    <li key={t} role="menuitem">
                      <button 
                        onClick={() => handleThemeChange(t)}
                        className="w-full text-left px-2 py-1 hover:bg-base-300"
                      >
                        {t}
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </li>
            <li>
              <button onClick={handleResetConversations}>Reset Conversations</button>
            </li>
          </ul>
        </div>
      </header>
      <main className="flex-1 h-[93vh] overflow-auto">
        {children}
      </main>
    </div>
  )
}

export default Layout