import { useState, useRef, useEffect } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import axios from 'axios'
import FileUpload from './FileUpload'
import MessageBubble from './MessageBubble'

export default function ChatInterface() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: '👋 Welcome! Upload an ArXiv PDF above and ask me anything about it. I\'ll answer using only what\'s in the papers — with citations.',
      sources: []
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [files, setFiles] = useState([])
  const bottomRef = useRef()

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() || loading) return
    const question = input.trim()
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: question }])
    setLoading(true)

    try {
      const res = await axios.post(`${import.meta.env.VITE_API_URL}/ask`, { question })
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: res.data.answer,
        sources: res.data.sources
      }])
    } catch (err) {
      const errorMsg = err.response?.data?.error || 'Something went wrong.'
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `❌ ${errorMsg}`,
        sources: []
      }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="gradient-bg min-h-screen flex flex-col items-center px-4 py-8">

      <div className="fixed top-0 left-0 w-96 h-96 bg-purple-600 rounded-full opacity-5 blur-3xl pointer-events-none" />
      <div className="fixed bottom-0 right-0 w-96 h-96 bg-blue-600 rounded-full opacity-5 blur-3xl pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-4xl mb-6"
      >
        <div className="glass-strong px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🔬</span>
            <div>
              <h1 className="text-white font-bold text-lg">ArXiv RAG Chatbot</h1>
              <p className="text-gray-500 text-xs">Powered by Gemini + FAISS</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
            <span className="text-gray-400 text-sm">
              {files.length > 0 ? `${files.length} paper(s) loaded` : 'No papers loaded'}
            </span>
          </div>
        </div>
      </motion.div>

      <div className="w-full max-w-4xl flex flex-col lg:flex-row gap-6 flex-1">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.1 }}
          className="lg:w-72 glass p-5 rounded-2xl h-fit"
        >
          <h2 className="text-white font-semibold mb-4 flex items-center gap-2">
            <span>📚</span> Upload Papers
          </h2>
          <FileUpload onFilesUpdate={setFiles} />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="flex-1 flex flex-col glass rounded-2xl overflow-hidden"
          style={{ height: '75vh' }}
        >
          <div className="flex-1 overflow-y-auto p-6">
            <AnimatePresence>
              {messages.map((msg, i) => (
                <MessageBubble key={i} message={msg} />
              ))}
            </AnimatePresence>

            {loading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex items-center gap-3 mb-4"
              >
                <div className="w-7 h-7 rounded-full bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-xs">
                  🤖
                </div>
                <div className="glass px-4 py-3 rounded-2xl rounded-tl-sm flex gap-2">
                  {[0, 1, 2].map(i => (
                    <motion.div
                      key={i}
                      animate={{ y: [0, -6, 0] }}
                      transition={{ duration: 0.6, repeat: Infinity, delay: i * 0.15 }}
                      className="w-2 h-2 bg-purple-400 rounded-full"
                    />
                  ))}
                </div>
              </motion.div>
            )}
            <div ref={bottomRef} />
          </div>

          <div className="p-4 border-t border-white border-opacity-10">
            <div className="flex gap-3">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                placeholder={files.length > 0
                  ? "Ask anything about your papers..."
                  : "Upload a paper first..."
                }
                disabled={files.length === 0 || loading}
                className="flex-1 bg-white bg-opacity-5 border border-white border-opacity-10
                  rounded-xl px-4 py-3 text-white placeholder-gray-600 text-sm
                  focus:outline-none focus:border-purple-500 transition-colors disabled:opacity-40"
              />
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={sendMessage}
                disabled={!input.trim() || loading || files.length === 0}
                className="px-5 py-3 rounded-xl text-white font-medium text-sm
                  disabled:opacity-40 disabled:cursor-not-allowed transition-all"
                style={{ background: 'linear-gradient(135deg, #667eea, #764ba2)' }}
              >
                Send →
              </motion.button>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}