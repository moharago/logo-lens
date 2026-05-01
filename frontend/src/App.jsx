import { useState } from 'react'
import Header from './components/Header'
import UploadSection from './components/UploadSection'
import ResultsGrid from './components/ResultsGrid'
import DetailsModal from './components/DetailsModal'
import './App.css'

export default function App() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [queryName, setQueryName] = useState('')
  const [selectedLogo, setSelectedLogo] = useState(null)

  const handleSearch = async (file) => {
    setLoading(true)
    setError(null)
    setQueryName(file.name)

    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch('/api/search?top_k=5', { method: 'POST', body: formData })
      if (!res.ok) throw new Error(`서버 오류 (${res.status})`)
      setResults(await res.json())
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <Header />
      <main className="main">
        <UploadSection onSearch={handleSearch} loading={loading} />
        {error && <p className="error-msg">{error}</p>}
        {loading && (
          <div className="loading">
            <div className="spinner" />
            <span>유사 로고를 검색 중입니다...</span>
          </div>
        )}
        {!loading && results && (
          <ResultsGrid results={results} queryName={queryName} onDetails={setSelectedLogo} />
        )}
      </main>
      {selectedLogo && (
        <DetailsModal logo={selectedLogo} onClose={() => setSelectedLogo(null)} />
      )}
    </div>
  )
}
