import './Header.css'

export default function Header() {
  return (
    <header className="header">
      <div className="header-inner">
        <div className="logo">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="12" cy="12" r="10" stroke="#1a56db" strokeWidth="2" />
            <circle cx="12" cy="12" r="5" fill="#1a56db" />
          </svg>
          <span className="logo-text">LOGO LENS</span>
        </div>
        <div
          className="user"
          role="button"
          tabIndex={0}
          onClick={() => {}}
          onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') e.currentTarget.click() }}
        >
          <div className="avatar">A</div>
          <span className="username">Alex Jeong</span>
          <span className="chevron">▾</span>
        </div>
      </div>
    </header>
  )
}
