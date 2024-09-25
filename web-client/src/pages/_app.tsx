import '../styles/globals.css'
import type { AppProps } from 'next/app'
import Layout from '../components/Layout'
import Head from 'next/head'
import { SecondaryWindowProvider } from '../components/SecondaryWindowContext'

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <SecondaryWindowProvider>
      <Head>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </SecondaryWindowProvider>
  )
}

export default MyApp