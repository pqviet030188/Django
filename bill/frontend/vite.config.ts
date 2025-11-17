/// <reference types="vitest" />
import { defineConfig as defineViteConfig, mergeConfig } from 'vite';
import { defineConfig as defineVitestConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import * as path from 'path';

// https://vite.dev/config/
const viteConfiig = defineViteConfig({
  resolve: {
    extensions: ['.js', '.jsx', '.ts', '.tsx', '.d.ts'],
    alias: [
      {
        find: '@components',
        replacement: path.resolve(__dirname, './src/components'),
      },
      {
        find: '@pages',
        replacement: path.resolve(__dirname, './src/pages'),
      },
    ],
  },
  plugins: [react()],
});

const vitestConfig = defineVitestConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/tests/setup.ts',
  },
});

export default mergeConfig(viteConfiig, vitestConfig);
