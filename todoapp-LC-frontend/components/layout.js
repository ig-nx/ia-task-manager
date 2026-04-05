import styles from '../styles/layout.module.css'

export default function Layout(props) {
  return (
    <div className={styles.layout}>
      <div className={styles.banner}>Panel de tareas</div>
      <h1 className={styles.title}>Tareas</h1>
      <div className={styles.content}>{props.children}</div>
      <footer className={styles.footer}>Organizador diario</footer>
    </div>
  )
}
