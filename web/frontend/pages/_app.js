import React, { useEffect } from "react";
import Head from "next/head";
import { ThemeProvider } from "@material-ui/core/styles";
import CssBaseline from "@material-ui/core/CssBaseline";
import { UserProvider } from "@/components/Providers/UserContext";
import { AuthProvider } from "@/components/Providers/AuthProvider";
import { theme } from "@/theme";
import i18n from "@/i18n";
import { I18nextProvider } from "react-i18next";
import { useRouter } from "next/router";
import { SWRConfig } from "swr";

function MyApp({ Component, pageProps }) {
  const router = useRouter();

  useEffect(() => {
    i18n.changeLanguage(router.locale);

    const jssStyles = document.querySelector("#jss-server-side");

    if (jssStyles) {
      jssStyles.parentElement.removeChild(jssStyles);
    }
  }, [router.locale]);

  return (
    <React.Fragment>
      <Head>
        <title>My page</title>
        <meta
          key="viewport"
          name="viewport"
          content="minimum-scale=1, initial-scale=1, width=device-width"
        />
      </Head>
      <I18nextProvider i18n={i18n}>
        <AuthProvider>
          <UserProvider>
            <ThemeProvider theme={theme}>
              {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
              <CssBaseline />
              <SWRConfig
                value={{
                  fetcher: (url, token = null, options = {}) => {
                    if (token) {
                      options.headers = {
                        Authorization: "Bearer " + token,
                      };
                    }

                    return fetch(
                      "http://localhost:8999/api/v1" + url,
                      options
                    ).then((res) => res.json());
                  },
                }}
              >
                <Component {...pageProps} />
              </SWRConfig>
            </ThemeProvider>
          </UserProvider>
        </AuthProvider>
      </I18nextProvider>
    </React.Fragment>
  );
}

export default MyApp;
