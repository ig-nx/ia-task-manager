import Head from 'next/head'
import Layout from '../components/layout';
import ToDoList from '../components/todo-list';

export default function Home() {
  return (
    <div>
      <Head>
        <title>Lista de Tareas</title>
        <meta name="description" content="Aplicacion de lista de tareas" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Layout>
        <ToDoList />
      </Layout>
    </div>
  )
}

