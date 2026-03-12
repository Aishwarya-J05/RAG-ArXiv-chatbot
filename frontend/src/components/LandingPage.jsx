import { motion } from 'framer-motion'

const features = [
  {
    icon: "🧠",
    title: "Semantic Search",
    desc: "FAISS vector database finds relevant context using meaning, not keywords"
  },
  {
    icon: "📄",
    title: "Multi-Paper Support",
    desc: "Upload multiple ArXiv papers and query across all of them simultaneously"
  },
  {
    icon: "🔗",
    title: "Source Citations",
    desc: "Every answer includes exact paper and page references — no hallucinations"
  },
  {
    icon: "⚡",
    title: "Gemini Powered",
    desc: "Google's latest Gemini model generates precise, grounded responses"
  }
]

export default function LandingPage({ onGetStarted }) {
  return (
    <div className="gradient-bg min-h-screen flex flex-col items-center justify-center px-6 py-20 relative overflow-hidden">

      <div className="absolute top-20 left-20 w-72 h-72 bg-purple-600 rounded-full opacity-10 blur-3xl" />
      <div className="absolute bottom-20 right-20 w-96 h-96 bg-blue-600 rounded-full opacity-10 blur-3xl" />
      <div className="absolute top-1/2 left-1/2 w-64 h-64 bg-pink-600 rounded-full opacity-5 blur-3xl" />

      <motion.div
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center max-w-4xl mx-auto mb-16"
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: "spring" }}
          className="text-6xl mb-6"
        >
          🔬
        </motion.div>

        <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
          Chat with{" "}
          <span className="gradient-text">ArXiv Papers</span>
        </h1>

        <p className="text-xl text-gray-400 mb-4 max-w-2xl mx-auto leading-relaxed">
          Upload AI research papers and ask questions. Get answers grounded
          in the actual papers — with source citations.
        </p>

        <p className="text-sm text-gray-600 mb-10">
          Powered by Google Gemini · FAISS Vector Search · RAG Architecture
        </p>

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={onGetStarted}
          className="px-10 py-4 rounded-full text-white font-semibold text-lg glow"
          style={{ background: "linear-gradient(135deg, #667eea, #764ba2)" }}
        >
          Start Researching →
        </motion.button>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto w-full">
        {features.map((f, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 + i * 0.1 }}
            whileHover={{ y: -5, scale: 1.02 }}
            className="glass p-6 text-center"
          >
            <div className="text-3xl mb-3">{f.icon}</div>
            <h3 className="text-white font-semibold mb-2">{f.title}</h3>
            <p className="text-gray-400 text-sm leading-relaxed">{f.desc}</p>
          </motion.div>
        ))}
      </div>
    </div>
  )
}