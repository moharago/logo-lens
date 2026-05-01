import './LogoCard.css'

export default function LogoCard({ logo, onDetails }) {
  const pct = Math.round(logo.score * 100)

  return (
    <div className="logo-card">
      <div className="card-image">
        <img
          src={`/api/logos/${logo._id}/image`}
          alt={logo.brand_name}
          onError={(e) => {
            e.target.style.display = 'none'
            e.target.parentElement.innerHTML = '<span class="img-fallback">No Image</span>'
          }}
        />
      </div>
      <div className="card-body">
        <p className="brand-name">{logo.brand_name}</p>
        <p className="score">{pct}%</p>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${pct}%` }} />
        </div>
        <button className="btn-details" onClick={() => onDetails(logo)}>
          Details
        </button>
      </div>
    </div>
  )
}
