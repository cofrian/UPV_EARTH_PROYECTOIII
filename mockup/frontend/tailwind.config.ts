import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        bg: "#040807",
        panel: "#0b1310",
        panelSoft: "#111b17",
        line: "#1e2d27",
        textMain: "#d9efe5",
        textMuted: "#93b0a3",
        accent: "#38a57a",
        accentSoft: "#1f694e"
      },
      boxShadow: {
        glow: "0 0 0 1px rgba(56,165,122,0.35), 0 12px 32px rgba(8,24,19,0.45)",
      }
    },
  },
  plugins: [],
};

export default config;
