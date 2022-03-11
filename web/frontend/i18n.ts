import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import LanguageDetector from "i18next-browser-languagedetector";
import ES from "@/public/locales/es/common.json";
import FR from "@/public/locales/fr/common.json";
import EN from "@/public/locales/en/common.json";

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    lng: "en",
    fallbackLng: "en",
    ns: ["common"],
    nsSeparator: ".",
    defaultNS: "common",
    resources: {
      en: {
        common: EN,
      },
      fr: {
        common: FR,
      },
      es: {
        common: ES,
      },
    },
    react: {
      useSuspense: false,
    },
  });

export default i18n;
