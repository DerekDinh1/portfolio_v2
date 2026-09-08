import { Link } from "react-router-dom";
import { STARTERS } from "../data/index.js";
import { MascotSprite } from "../shared.jsx";

export default function NotFound() {
  const starter = STARTERS[2];
  return (
    <main className="page theme-grass">
      <div className="wrap notfound">
        <MascotSprite
          starter={starter}
          loop="idle"
          className="notfound-mascot"
          alt={`${starter.name} looking a little lost`}
        />
        <h1>Looks like you wandered off the trail.</h1>
        <p>That path doesn't lead anywhere. Not even {starter.name} knows this one. Let's head back to the lab.</p>
        <Link className="btn btn-red" to="/">← Back to the lab</Link>
      </div>
    </main>
  );
}
