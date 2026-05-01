import LogoCard from './LogoCard'
import './ResultsGrid.css'

export default function ResultsGrid({ results, queryName, onDetails }) {
  return (
    <section className="results-section">
      <div className="results-header">
        <h2 className="section-title">SEARCH RESULTS</h2>
        <p className="results-summary">
          <strong>{results.count}</strong> SIMILAR LOGOS FOUND
          {queryName && <span className="query-name"> (Query: {queryName})</span>}
        </p>
      </div>
      <div className="results-grid">
        {results.results.map((logo) => (
          <LogoCard key={logo._id} logo={logo} onDetails={onDetails} />
        ))}
      </div>
    </section>
  )
}
