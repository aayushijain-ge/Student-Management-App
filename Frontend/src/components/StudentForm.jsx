import { useState } from "react";

function StudentForm({ initialData, onSubmit, onCancel, saving }) {
  const [form, setForm] = useState(
    initialData || { name: "", age: "", course: "" }
  );

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      name: form.name.trim(),
      age: Number(form.age),
      course: form.course.trim(),
    });
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      <label>
        Name
        <input
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="Enter name"
          required
        />
      </label>

      <label>
        Age
        <input
          name="age"
          type="number"
          min="1"
          value={form.age}
          onChange={handleChange}
          placeholder="Enter age"
          required
        />
      </label>

      <label>
        Course
        <input
          name="course"
          value={form.course}
          onChange={handleChange}
          placeholder="Enter course"
          required
        />
      </label>

      <div className="form-actions">
        <button type="button" className="btn btn-light" onClick={onCancel}>
          Cancel
        </button>
        <button type="submit" className="btn btn-primary" disabled={saving}>
          {saving ? "Saving..." : initialData ? "Update" : "Add Student"}
        </button>
      </div>
    </form>
  );
}

export default StudentForm;