function verifyAdmin() {
  const adminCode = prompt("لطفا کد مدیریت را وارد کنید:");

  const correctCode = "1234";

  if (adminCode === correctCode) {
    window.location.href = "/edit";
  } else {
    alert("کد نادرست است. لطفا دوباره امتحان کنید.");
  }
}

document.addEventListener("DOMContentLoaded", function () {
  // Automatically load data when the page loads
  loadDataForDate();

  // Save data every time a selection is changed
  document.querySelectorAll('.unit-select').forEach(select => {
    select.addEventListener('change', saveSelection); // Attach saveSelection to the change event
  });

  // Save the current selections to the selected date
  function saveSelection() {
    const selections = {};
    const selectedDate = document.getElementById('selected-date').value;

    // Collect all selections
    document.querySelectorAll('.meal-section').forEach(mealSection => {
      const mealName = mealSection.querySelector('h3').innerText.trim(); // Get meal name (e.g., "breakfast", "lunch")
      selections[mealName] = {}; // Initialize meal category

      mealSection.querySelectorAll('.category-item').forEach(categoryItem => {
        const category = categoryItem.querySelector('label').innerText.trim(); // Get category name (e.g., "پروتئین")

        categoryItem.querySelectorAll('.unit-select').forEach(select => {
          const selectedValue = select.value;
          if (selectedValue) {
            if (!selections[mealName][category]) {
              selections[mealName][category] = [];
            }
            selections[mealName][category].push(selectedValue); // Save selected values under the correct meal and category
          }
        });
      });
    });

    // Save selections automatically via POST request
    fetch(`/save-selections/${selectedDate}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(selections),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Selections saved successfully!');
      })
      .catch(error => {
        console.error('Error saving data:', error);
      });
  }

  // Load data when the date changes
  document.getElementById('selected-date').addEventListener('change', loadDataForDate);

  // Load data for the selected date
  function loadDataForDate() {
    const selectedDate = document.getElementById('selected-date').value;

    // Fetch data for the selected date
    fetch(`/load-selections/${selectedDate}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('No data for this date');
        }
        return response.json();
      })
      .then(data => {
        // Clear current selections
        document.querySelectorAll('.unit-select').forEach(select => {
          select.value = "";  // Reset the current selections
        });

        // Fill the form with loaded data
        document.querySelectorAll('.meal-section').forEach(mealSection => {
          const mealName = mealSection.querySelector('h3').innerText.trim(); // Get meal name

          if (data[mealName]) {
            mealSection.querySelectorAll('.category-item').forEach(categoryItem => {
              const category = categoryItem.querySelector('label').innerText.trim();

              if (data[mealName][category] && data[mealName][category].length > 0) {
                categoryItem.querySelectorAll('.unit-select').forEach((select, index) => {
                  if (data[mealName][category][index]) {
                    select.value = data[mealName][category][index]; // Set the value from the loaded data
                  }
                });
              }
            });
          }
        });
      })
      .catch(error => {
        console.error('Error loading data:', error);
        alert('داده‌ای برای این تاریخ وجود ندارد');
      });
  }
});
