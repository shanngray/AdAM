import '../styles/globals.css'
import type { AppProps } from 'next/app'
import Layout from '../components/Layout'
import Head from 'next/head'
import { SecondaryWindowProvider } from '../components/SecondaryWindowContext'
import { SelectedConversationProvider } from '../components/SelectedConversationContext'

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <SelectedConversationProvider>
      <SecondaryWindowProvider>
        <Head>
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <Layout>
          <Component {...pageProps} />
        </Layout>
      </SecondaryWindowProvider>
    </SelectedConversationProvider>
  )
}

export default MyApp