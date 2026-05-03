import { useState, useRef, useCallback, useEffect } from 'react'
import './UploadSection.css'

export default function UploadSection({ onSearch, loading }) {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [dragging, setDragging] = useState(false)
  const inputRef = useRef()

  useEffect(() => {
    return () => { if (preview) URL.revokeObjectURL(preview) }
  }, [preview])

  const handleFile = (f) => {
    if (!f) return
    setFile(f)
    if (preview) URL.revokeObjectURL(preview)
    setPreview(URL.createObjectURL(f))
  }

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setDragging(false)
    const f = e.dataTransfer.files[0]
    if (f && f.type.startsWith('image/')) handleFile(f)
  }, [])

  const handleDragOver = (e) => { e.preventDefault(); setDragging(true) }
  const handleDragLeave = () => setDragging(false)

  return (
    <section className="upload-section">
      <h2 className="section-title">SEARCH LOGO</h2>
      <div className="upload-card">
        <div className="upload-label">UPLOAD YOUR LOGO</div>
        <div
          className={`dropzone ${dragging ? 'dragging' : ''} ${preview ? 'has-preview' : ''}`}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onClick={() => !preview && inputRef.current.click()}
        >
          {preview ? (
            <img src={preview} alt="preview" className="preview-img" />
          ) : (
            <>
              <svg className="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M12 16V8m0 0-3 3m3-3 3 3" strokeLinecap="round" strokeLinejoin="round" />
                <rect x="3" y="3" width="18" height="18" rx="3" strokeLinejoin="round" />
              </svg>
              <p className="drop-text">Drag & Drop Query Logo Here</p>
              <button
                className="btn-upload"
                onClick={(e) => { e.stopPropagation(); inputRef.current.click() }}
              >
                Upload File
              </button>
              <p className="hint">Supported: PNG, JPG, JPEG (Max 10MB)</p>
            </>
          )}
        </div>

        <input
          ref={inputRef}
          type="file"
          accept="image/png,image/jpeg,image/jpg"
          hidden
          onChange={(e) => handleFile(e.target.files[0])}
        />

        {preview && (
          <div className="upload-actions">
            <button className="btn-change" onClick={() => inputRef.current.click()}>
              파일 변경
            </button>
            <button
              className="btn-search"
              onClick={() => onSearch(file)}
              disabled={loading}
            >
              {loading ? '검색 중...' : '검색'}
            </button>
          </div>
        )}
      </div>
    </section>
  )
}
