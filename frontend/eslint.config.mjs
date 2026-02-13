import { FlatCompat } from "@eslint/eslintrc";

import { dirname } from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
    baseDirectory: __dirname,
});

const eslintConfig = [
    {
        ignores: [".next/**", "node_modules/**"],
    },
    ...compat.extends("next/core-web-vitals", "next/typescript"),
    {
        rules: {
            // Enforce 4-space indentation
            indent: ["error", 4],
            "react/jsx-first-prop-new-line": ["error", "multiline-multiprop"],
            "react/jsx-max-props-per-line": ["error", { "maximum": 1 }],
            "@typescript-eslint/no-explicit-any": "off",
            "import/order": [
                "error",
                {
                    "groups": [
                        "external",
                        "builtin",
                        "internal",
                        "sibling",
                        "parent",
                        "index"
                    ],
                    "newlines-between": "always",
                },
            ],
        },
    },
];

export default eslintConfig;
