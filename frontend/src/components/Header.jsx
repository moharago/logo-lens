import './Header.css'

export default function Header() {
  return (
    <header className="header">
      <div className="header-inner">
        <div className="logo">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="10" stroke="#1a56db" strokeWidth="2" />
            <circle cx="12" cy="12" r="5" fill="#1a56db" />
          </svg>
          <span className="logo-text">LOGO LENS</span>
        </div>
        <div className="user">
          <div className="avatar">A</div>
          <span className="username">Alex Jeong</span>
          <span className="chevron">▾</span>
        </div>
      </div>
    </header>
  )
}
