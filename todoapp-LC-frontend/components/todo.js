// import Image from 'next/image'
// import styles from '../styles/todo.module.css'
// import { useState, useEffect } from 'react'
// import { createPortal } from 'react-dom'

// export default function ToDo(props) {
//   const { todo, onChange, onDelete } = props;
//   const [poem, setPoem] = useState(null);
//   const [isPoemVisible, setIsPoemVisible] = useState(false);
//   const [mounted, setMounted] = useState(false);

//   useEffect(() => {
//     setMounted(true);
//   }, []);

//   // The following function is added for our LangChain test:
//   async function generatePoem(id) {
//     const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/todos/write-poem/${id}`, {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//       });
  
//     if (res.ok) {
//         const data = await res.json();
//         setPoem(data.poem);
//         setIsPoemVisible(true); // Show the poem box when a poem is generated
//     }
//   }

//   // Function to close the poem box
//   function closePoemBox() {
//     setIsPoemVisible(false);
//   }

//   return (
//     <>
//       <div className={styles.toDoRow} key={todo.id}>
//         <input
//           className={styles.toDoCheckbox}
//           name="completed"
//           type="checkbox"
//           checked={todo.completed}
//           value={todo.completed}
//           onChange={(e) => onChange(e, todo.id)}
//         ></input>
//         <input
//           className={styles.todoInput}
//           autoComplete='off'
//           name="name"
//           type="text"
//           value={todo.name}
//           onChange={(e) => onChange(e, todo.id)}
//         ></input>
//         <button
//           className={styles.generatePoemBtn}
//           onClick={() => generatePoem(todo.id)}
//         >
//           Generate Poem
//         </button>
//         <button className={styles.deleteBtn} onClick={() => onDelete(todo.id)}>
//           <Image src="/delete-outline.svg" width="24" height="24" />
//         </button>
//       </div>
//       {isPoemVisible && mounted && createPortal(
//         <>
//           <div className={styles.overlay} onClick={closePoemBox}></div>
//           <div className={styles.poemBox}>
//             <button className={styles.closeButton} onClick={closePoemBox}>
//               &times;
//             </button>
//             <div className={styles.poem}>
//               <p>{poem}</p>
//             </div>
//           </div>
//         </>,
//         document.body
//       )}
//     </>
//   );  

// }












import Image from 'next/image'
import styles from '../styles/todo.module.css'
import { useState } from 'react'

export default function TodoItem(props) {
  const { todo, onChange, onDelete } = props;
  
  // NUEVO: Estado relacionado con la IA
  const [poem, setPoem] = useState(null);
  const [isPoemVisible, setIsPoemVisible] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState(null);

  // NUEVO: FunciÃ³n para la generaciÃ³n del poema con IA
  async function generatePoem(id) {
    if (isGenerating) return;
    
    try {
      setIsGenerating(true);
      setError(null);
      
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/todos/write-poem/${id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        setPoem(data.poem);
        setIsPoemVisible(true);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Fallo al generar el poema');
      }
    } catch (error) {
      console.error('Error en la generaciÃ³n del poema:', error);
      setError('No se pudo conectar al servicio de IA. Por favor, intÃ©ntalo de nuevo.');
    } finally {
      setIsGenerating(false);
    }
  }

  // NUEVO: Cerrar el popup del poema
  function closePoemBox() {
    setIsPoemVisible(false);
  }

  return (
    <>
      {/* Fila principal de la tarea (funcionalidad existente + nuevo botÃ³n) */}
      <div className={styles.todoRow}>
        {/* Elementos existentes sin cambios */}
        <input
          className={styles.todoCheckbox}
          name="completed"
          type="checkbox"
          checked={todo.completed}
          onChange={(e) => onChange(e, todo.id)}
        />
        <input
          className={styles.todoInput}
          autoComplete='off'
          name="name"
          type="text"
          value={todo.name}
          onChange={(e) => onChange(e, todo.id)}
        />
        
        {/* NUEVO: BotÃ³n Generar Poema */}
        <button
          className={styles.generatePoemBtn}
          onClick={() => generatePoem(todo.id)}
          disabled={isGenerating}
        >
          {isGenerating ? 'Generando...' : 'Generar Poema'}
        </button>
        
        {/* BotÃ³n de eliminar existente sin cambios */}
        <button className={styles.deleteBtn} onClick={() => onDelete(todo.id)}>
          <Image src="/delete-outline.svg" width="24" height="24" alt="Eliminar" />
        </button>
      </div>
      
      {/* NUEVO: Popup del poema */}
      {isPoemVisible && (
        <div className={styles.poemOverlay}>
          <div className={styles.poemBox}>
            <button 
              className={styles.closeButton} 
              onClick={closePoemBox}
            >
              &times;
            </button>
            <h3 className={styles.poemTitle}>Poema Generado por IA</h3>
            <div className={styles.poem}>
              <p>{poem}</p>
            </div>
          </div>
        </div>
      )}
      
      {/* NUEVO: Pantalla de mensaje de error */}
      {error && (
        <div className={styles.errorMessage}>
          {error}
          <button onClick={() => setError(null)}>Ã—</button>
        </div>
      )}
    </>
  );
}

