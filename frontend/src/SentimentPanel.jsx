/**
 * Gemini's streamer and chat sentiment for a paid tip.
 */
import { fmtScore, moodClass } from './format.js'

export default function SentimentPanel({ analysis }) {
  if (!analysis) return null
  const { streamer, chat } = analysis
  return (
    <div className="sentiment">
      <div className="sentiment-row">
        <span className="sentiment-who">Streamer</span>
        <span className={`pill ${moodClass(streamer.score)}`}>{streamer.label} {fmtScore(streamer.score)}</span>
        {streamer.emotions?.map((e) => <span key={e} className="pill">{e}</span>)}
        <span className="muted small-inline">brand: {streamer.brand_attitude}</span>
        <div className="muted small-inline sentiment-detail">
          {streamer.summary} Voice: {streamer.tone_of_voice}. Face: {streamer.facial_expression}.
        </div>
      </div>
      <div className="sentiment-row">
        <span className="sentiment-who">Chat</span>
        {chat ? (
          <>
            <span className={`pill ${moodClass(chat.score)}`}>{chat.label} {fmtScore(chat.score)}</span>
            <span className="pill">{Math.round(chat.positive_share * 100)}% positive</span>
            {chat.themes?.map((t) => <span key={t} className="pill">{t}</span>)}
            <div className="muted small-inline sentiment-detail">{chat.summary}</div>
          </>
        ) : (
          <span className="muted small-inline">no chat around this moment</span>
        )}
      </div>
    </div>
  )
}
