import { motion } from 'framer-motion'

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user'

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
    >
      <div className={`max-w-[80%] ${isUser ? 'items-end' : 'items-start'} flex flex-col gap-2`}>
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

        <div
          className={`px-5 py-3 rounded-2xl text-sm leading-relaxed
            ${isUser
              ? 'text-white rounded-tr-sm'
              : 'glass text-gray-200 rounded-tl-sm'
            }`}
          style={isUser ? {
            background: 'linear-gradient(135deg, #667eea, #764ba2)'
          } : {}}
        >
          {message.content}
        </div>

        {message.sources && message.sources.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="flex flex-wrap gap-2 mt-1"
          >
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