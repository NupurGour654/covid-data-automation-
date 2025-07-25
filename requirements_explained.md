#  Project Dependencies – Why These Libraries Are Used

Below is a list of Python libraries used in this COVID data automation project along with brief explanations:

---

### 1. `pandas`
- **Why needed:** Used for reading, cleaning, and manipulating structured data.
- **In this project:** Loads COVID CSV data, processes country-wise stats, filters and transforms columns.

---

### 2. `matplotlib`
- **Why needed:** Used for basic data visualization (line charts, bar plots, etc.)
- **In this project:** Plots trends like total cases over time, daily increase/decrease, etc.

---

### 3. `seaborn`
- **Why needed:** Built on top of matplotlib for more aesthetic and informative plots.
- **In this project:** For advanced plotting like heatmaps, barplots, distribution graphs.

---

### 4. `numpy`
- **Why needed:** For numerical operations and efficient array handling.
- **In this project:** Not always mandatory, but used during calculations like moving averages or ratios.

---

### 5. `requests` *(optional, if used)*
- **Why needed:** To make HTTP requests (like downloading CSV from a URL).
- **In this project:** Used if you're automating the data download from Our World in Data.

---

### 6. `datetime`
- **Why needed:** For handling and formatting dates during analysis.
- **In this project:** Helps format dates, filter recent records, and calculate time intervals.

---

