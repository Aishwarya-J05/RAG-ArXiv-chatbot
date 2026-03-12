import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import LandingPage from './components/LandingPage'
import ChatInterface from './components/ChatInterface'

export default function App() {
  const [started, setStarted] = useState(false)

  return (
    <AnimatePresence mode="wait">
      {!started ? (
        <motion.div
          key="landing"
          exit={{ opacity: 0, y: -40 }}
          transition={{ duration: 0.5 }}
        >
          <LandingPage onGetStarted={() => setStarted(true)} />
        </motion.div>
      ) : (
        <motion.div
          key="chat"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <ChatInterface />
        </motion.div>
      )}
    </AnimatePresence>
  )
}