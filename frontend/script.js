let tasks = [];

function addTask() {
  const name = document.getElementById("taskName").value;
  const duration = parseInt(document.getElementById("taskDuration").value);

  if (!name || !duration) return;

  tasks.push({ name, duration });

  const li = document.createElement("li");
  li.innerText = `${name} - ${duration}h`;
  document.getElementById("taskList").appendChild(li);
}

async function generate() {
  const res = await fetch("http://127.0.0.1:8000/timetable/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      tasks: tasks,
      start: 6
    })
  });

  const data = await res.json();

  const output = document.getElementById("output");
  output.innerHTML = "";

  data.schedule.forEach(item => {
    const div = document.createElement("div");
    div.innerText = `${item.task}: ${item.start}:00 - ${item.end}:00`;
    output.appendChild(div);
  });
}