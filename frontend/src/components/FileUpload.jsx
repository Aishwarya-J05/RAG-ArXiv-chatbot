import { useState, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'

export default function FileUpload({ onFilesUpdate }) {
  const [uploading, setUploading] = useState(false)
  const [files, setFiles] = useState([])
  const [dragOver, setDragOver] = useState(false)
  const inputRef = useRef()

  const uploadFile = async (file) => {
    if (!file.name.endsWith('.pdf')) {
      alert('Please upload PDF files only')
      return
    }
    setUploading(true)
    const formData = new FormData()
    formData.append('file', file)
    try {
      const res = await axios.post('http://localhost:8000/upload', formData)
      const updatedFiles = res.data.files
      setFiles(updatedFiles)
      onFilesUpdate(updatedFiles)
    } catch (err) {
      console.error('Upload failed:', err)
      alert('Upload failed. Is the backend running?')
    } finally {
      setUploading(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragOver(false)
    const file = e.dataTransfer.files[0]
    if (file) uploadFile(file)
  }

  return (
    <div className="w-full">
      <motion.div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current.click()}
        animate={{
          borderColor: dragOver ? '#667eea' : 'rgba(255,255,255,0.1)',
          background: dragOver ? 'rgba(102,126,234,0.1)' : 'rgba(255,255,255,0.03)'
        }}
        className="border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all"
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={(e) => uploadFile(e.target.files[0])}
        />
        {uploading ? (
          <div className="flex flex-col items-center gap-3">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              className="w-8 h-8 border-2 border-purple-500 border-t-transparent rounded-full"
            />
            <p className="text-gray-400 text-sm">Processing & embedding PDF...</p>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-3">
            <div className="text-4xl">📄</div>
            <p className="text-white font-medium">Drop PDF here or click to upload</p>
            <p className="text-gray-500 text-sm">ArXiv papers work best</p>
          </div>
        )}
      </motion.div>

      <AnimatePresence>
        {files.length > 0 && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            className="mt-4 space-y-2"
          >
            <p className="text-gray-500 text-xs uppercase tracking-wider mb-2">
              Loaded Papers
            </p>
            {files.map((f, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.1 }}
                className="flex items-center gap-3 glass p-3 rounded-xl"
              >
                <span className="text-green-400 text-sm">✓</span>
                <span className="text-gray-300 text-sm truncate">{f}</span>
              </motion.div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}