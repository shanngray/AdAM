import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
    },
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark", "cupcake", "lemonade",
    {
      mytheme: {        
        "primary": "#6700FF",
        "secondary": "#3B0091",
        "accent": "#4C00BC",
        "neutral": "#E3F0FF",
        "base-100": "#FBFAFF",
        "info": "#0000ff",
        "success": "#166534",
        "warning": "#f43f5e",
        "error": "#ff0000", 
        },
      },
    ], // Add your preferred themes here
  },
};
export default config;