import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <main className="page">
      <div className="wrap notfound">
        <h1>A wild 404 appeared!</h1>
        <p>That path got away. Let's head back to the lab.</p>
        <Link className="btn btn-red" to="/">← Back to the lab</Link>
      </div>
    </main>
  );
}
