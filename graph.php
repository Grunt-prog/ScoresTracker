<?php
// Database connection
$servername = "127.0.0.1";
$username = "root";
$password = "";
$database = "student";
$port = 3307;

$conn = new mysqli($servername, $username, $password, $database, $port);
if($conn->connect_error){
    die('connection Failed: '.connect_error);
}else{
    echo "success";
}

// Retrieve input values from the query parameters
$rollNo = $_POST['rollNo'];
$semester = $_POST['semester'];

// Query the database to fetch subject-wise grades based on roll number and semester
$query = "SELECT subject, grade FROM grades_table WHERE roll_no = '$rollNo' AND semester = '$semester'";
$result = $conn->query($query);

// Fetch subject-wise grades and store them in an array
$gradesData = [];
while ($row = $result->fetch_assoc()) {
    $gradesData[] = [
        'subject' => $row['subject'],
        'grade' => $row['grade']
    ];
}

// Convert the grades data to JSON format to be used in JavaScript
$gradesJson = json_encode($gradesData);
?>

<!DOCTYPE html>
<html>
<head>
    <title>Graph</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <script>
        // JavaScript code to render the table and charts
        var gradesData = <?php echo $gradesJson; ?>;

        // Render the table
        var tableBody = document.querySelector('#gradesTable tbody');
        gradesData.forEach(function(data) {
            var row = document.createElement('tr');
            var subjectCell = document.createElement('td');
            subjectCell.textContent = data.subject;
            var gradeCell = document.createElement('td');
            gradeCell.textContent = data.grade;
            row.appendChild(subjectCell);
            row.appendChild(gradeCell);
            tableBody.appendChild(row);
        });

        // Render the bar chart
        var barChartCanvas = document.getElementById('barChart').getContext('2d');
        var barChart = new Chart(barChartCanvas, {
            type: 'bar',
            data: {
                labels: gradesData.map(function(data) { return data.subject; }),
                datasets: [{
                    label: 'Grades',
                    data: gradesData.map(function(data) { return data.grade; }),
                    backgroundColor: 'rgba(0, 123, 255, 0.5)',
                    borderColor: 'rgba(0, 123, 255, 1)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Grade'
                        }
                    }
                }
            }
        });

        // Placeholder code for the performance across semesters graph
        var lineChartCanvas = document.getElementById('lineChart').getContext('2d');
        var lineChart = new Chart(lineChartCanvas, {
            // Configure the line chart as needed
        });
    </script>

    <div>
        <h2>Subject-wise Performance</h2>
        <table id="gradesTable">
            <thead>
                <tr>
                    <th>Subject</th>
                    <th>Grade</th>
                </tr>
            </thead>
            <tbody>
                <!-- Table rows will be dynamically populated using JavaScript -->
            </tbody>
        </table>
    </div>

    <div>
        <h2>Subject-wise Performance Bar Graph</h2>
        <canvas id="barChart"></canvas>
    </div>

    <div>
        <h2>Performance across Semesters</h2>
        <canvas id="lineChart"></canvas>
    </div>
</body>
</html>
