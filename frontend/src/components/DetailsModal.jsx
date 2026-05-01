import './DetailsModal.css'

export default function DetailsModal({ logo, onClose }) {
  const pct = Math.round(logo.score * 100)

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Logo Details</h3>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>
        <div className="modal-body">
          <div className="modal-image">
            <img
              src={`/api/logos/${logo._id}/image`}
              alt={logo.brand_name}
            />
          </div>
          <table className="detail-table">
            <tbody>
              <tr>
                <th>Brand</th>
                <td>{logo.brand_name}</td>
              </tr>
              <tr>
                <th>Similarity</th>
                <td><span className="score-badge">{pct}%</span></td>
              </tr>
              <tr>
                <th>Tags</th>
                <td>
                  {logo.tags?.length ? (
                    <div className="tags">
                      {logo.tags.map((t) => (
                        <span key={t} className="tag">{t}</span>
                      ))}
                    </div>
                  ) : <span className="empty">—</span>}
                </td>
              </tr>
              <tr>
                <th>ID</th>
                <td className="mono">{logo._id}</td>
              </tr>
              {logo.created_at && (
                <tr>
                  <th>등록일</th>
                  <td>{new Date(logo.created_at).toLocaleDateString('ko-KR')}</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
