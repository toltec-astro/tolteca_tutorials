import shared from '../../slides/marp.config.mjs';
import { fileURLToPath } from 'node:url';

export default {
  ...shared,
  themeSet: fileURLToPath(new URL('./theme.css', import.meta.url)),
};
