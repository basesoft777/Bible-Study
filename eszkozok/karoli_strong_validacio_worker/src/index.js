// F175.V21 — a validációs Worker belépési pontja; a logika: logika.js.
import { kezel } from './logika.js';

export default {
  fetch(req, env) { return kezel(req, env); },
};
