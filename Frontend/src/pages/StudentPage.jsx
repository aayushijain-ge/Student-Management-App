import { useEffect, useState } from "react";
import {
  getStudents,
  createStudent,
  updateStudent,
  deleteStudent,
} from "../api/studentApi";
import Modal from "../components/Modal";
import StudentForm from "../components/StudentForm";
import StudentTable from "../components/StudentTable";

function StudentsPage() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [search, setSearch] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState(null);

  const showMessage = (text) => {
    setMessage(text);
    setTimeout(() => setMessage(""), 2500);
  };

  const fetchStudents = async () => {
    try {
      setLoading(true);
      setError("");
      const res = await getStudents();
      setStudents(res.data);
    } catch (err) {
      setError("Could not load students. Is the backend running?");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  const openAdd = () => {
    setEditing(null);
    setModalOpen(true);
  };

  const openEdit = (student) => {
    setEditing(student);
    setModalOpen(true);
  };

  const closeModal = () => {
    setModalOpen(false);
    setEditing(null);
  };

  const handleSubmit = async (data) => {
    try {
      setSaving(true);
      if (editing) {
        await updateStudent(editing.id, data);
        showMessage("Student updated successfully");
      } else {
        await createStudent(data);
        showMessage("Student added successfully");
      }
      closeModal();
      fetchStudents();
    } catch (err) {
      setError("Could not save the student.");
      console.error(err);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (student) => {
    if (!window.confirm(`Delete ${student.name}?`)) return;
    try {
      await deleteStudent(student.id);
      showMessage("Student deleted successfully");
      fetchStudents();
    } catch (err) {
      setError("Could not delete the student.");
      console.error(err);
    }
  };

  const filtered = students.filter(
    (s) =>
      s.name.toLowerCase().includes(search.toLowerCase()) ||
      s.course.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="container">
      <header className="header">
        <div>
          <h1>Student Management</h1>
          <p className="muted">{students.length} students total</p>
        </div>
        <button className="btn btn-primary" onClick={openAdd}>
          + Add Student
        </button>
      </header>

      {message && <div className="alert alert-success">{message}</div>}
      {error && <div className="alert alert-error">{error}</div>}

      <div className="card">
        <input
          className="search"
          placeholder="Search by name or course..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        {loading ? (
          <p className="empty">Loading...</p>
        ) : (
          <StudentTable
            students={filtered}
            onEdit={openEdit}
            onDelete={handleDelete}
          />
        )}
      </div>

      {modalOpen && (
        <Modal
          title={editing ? "Edit Student" : "Add Student"}
          onClose={closeModal}
        >
          <StudentForm
            initialData={
              editing
                ? { name: editing.name, age: editing.age, course: editing.course }
                : null
            }
            onSubmit={handleSubmit}
            onCancel={closeModal}
            saving={saving}
          />
        </Modal>
      )}
    </div>
  );
}

export default StudentsPage;