import { motion } from 'framer-motion'
import ReactMarkdown from 'react-markdown'

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user'

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-6`}
    >
      <div className={`max-w-[85%] flex flex-col gap-2 ${isUser ? 'items-end' : 'items-start'}`}>

        {/* Avatar + name */}
        <div className={`flex items-center gap-2 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
          <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs
            ${isUser
              ? 'bg-gradient-to-br from-purple-500 to-pink-500'
              : 'bg-gradient-to-br from-blue-500 to-cyan-500'
            }`}
          >
            {isUser ? '👤' : '🤖'}
          </div>
          <span className="text-gray-500 text-xs">
            {isUser ? 'You' : 'RAG Assistant'}
          </span>
        </div>

        {/* Bubble */}
        <div
          className={`px-5 py-4 rounded-2xl text-sm leading-relaxed w-full
            ${isUser
              ? 'text-white rounded-tr-sm'
              : 'glass text-gray-200 rounded-tl-sm'
            }`}
          style={isUser ? {
            background: 'linear-gradient(135deg, #667eea, #764ba2)'
          } : {}}
        >
          {isUser ? (
            <p>{message.content}</p>
          ) : (
            <ReactMarkdown
              components={{
                h1: ({ children }) => (
                  <h1 className="text-lg font-bold text-white mt-3 mb-2 pb-1"
                    style={{ borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                    {children}
                  </h1>
                ),
                h2: ({ children }) => (
                  <h2 className="text-base font-bold text-purple-300 mt-4 mb-2">
                    {children}
                  </h2>
                ),
                h3: ({ children }) => (
                  <h3 className="text-sm font-bold text-blue-300 mt-3 mb-1">
                    {children}
                  </h3>
                ),
                p: ({ children }) => (
                  <p className="text-gray-200 leading-relaxed mb-3 last:mb-0">
                    {children}
                  </p>
                ),
                ul: ({ children }) => (
                  <ul className="mb-3 space-y-1.5 mt-1">
                    {children}
                  </ul>
                ),
                ol: ({ children }) => (
                  <ol className="mb-3 space-y-1.5 mt-1 list-decimal list-inside">
                    {children}
                  </ol>
                ),
                li: ({ children }) => (
                  <li className="text-gray-200 leading-relaxed flex gap-2 items-start">
                    <span className="text-purple-400 mt-0.5 flex-shrink-0 text-xs">▸</span>
                    <span>{children}</span>
                  </li>
                ),
                strong: ({ children }) => (
                  <strong className="font-semibold text-white">{children}</strong>
                ),
                em: ({ children }) => (
                  <em className="italic text-gray-300">{children}</em>
                ),
                code: ({ inline, children }) =>
                  inline ? (
                    <code
                      className="px-1.5 py-0.5 rounded text-xs font-mono"
                      style={{
                        background: 'rgba(102,126,234,0.2)',
                        color: '#a78bfa',
                        border: '1px solid rgba(102,126,234,0.3)'
                      }}
                    >
                      {children}
                    </code>
                  ) : (
                    <pre
                      className="rounded-xl p-4 my-3 overflow-x-auto text-xs font-mono leading-relaxed"
                      style={{ background: 'rgba(0,0,0,0.4)', color: '#e2e8f0' }}
                    >
                      <code>{children}</code>
                    </pre>
                  ),
                blockquote: ({ children }) => (
                  <blockquote
                    className="pl-4 my-3 italic text-gray-400"
                    style={{ borderLeft: '2px solid #7c3aed' }}
                  >
                    {children}
                  </blockquote>
                ),
                hr: () => (
                  <hr className="my-4" style={{ borderColor: 'rgba(255,255,255,0.1)' }} />
                ),
              }}
            >
              {message.content}
            </ReactMarkdown>
          )}
        </div>

        {/* Source citations */}
        {message.sources && message.sources.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="flex flex-wrap gap-2 mt-1 items-center"
          >
            <span className="text-gray-600 text-xs">Sources:</span>
            {message.sources.map((source, i) => (
              <span
                key={i}
                className="text-xs px-3 py-1 rounded-full"
                style={{
                  background: 'rgba(102, 126, 234, 0.15)',
                  border: '1px solid rgba(102, 126, 234, 0.3)',
                  color: '#a78bfa'
                }}
              >
                📎 {source}
              </span>
            ))}
          </motion.div>
        )}
      </div>
    </motion.div>
  )
}