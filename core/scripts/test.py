
from core.models import IOTQuestion  # 🔁 Replace 'your_app' with your actual Django app name
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "misstantra.settings")  # 🔁 Replace 'myproject' with your project name
django.setup()



questions_data = [
            ("Which component of BI converts raw data into useful insights?", "Analytics Engine", "Database Server", "Web Server", "Firewall", "Analytics Engine"),
            ("OLTP systems are mainly used for?", "Daily transactions", "Data analysis", "Predictive modeling", "Data mining", "Daily transactions"),
            ("OLAP systems are best suited for?", "Complex queries", "Simple updates", "Real-time transactions", "Log management", "Complex queries"),
            ("Which layer in BI architecture handles data transformation?", "ETL Layer", "Presentation Layer", "Storage Layer", "Application Layer", "ETL Layer"),
            ("Dashboards in BI are used to?", "Visualize data", "Store data", "Encrypt data", "Delete data", "Visualize data"),
            ("What is the main goal of BI?", "Informed decision-making", "Increase data storage", "Speed up coding", "Secure files", "Informed decision-making"),
            ("Which tool is commonly used for BI?", "Power BI", "Notepad", "Excel Paint", "Adobe PDF", "Power BI"),
            ("ETL stands for?", "Extract Transform Load", "Encrypt Transfer Log", "Erase Test Learn", "Extend Transfer Link", "Extract Transform Load"),
            ("In BI, data warehouse stores?", "Historical data", "Temporary files", "Executable code", "Source data", "Historical data"),
            ("Data visualization mainly focuses on?", "Graphical representation", "Data encryption", "Backup creation", "API calls", "Graphical representation"),
            ("Which BI tool uses worksheets and dashboards?", "Tableau", "GitHub", "Slack", "Postman", "Tableau"),
            ("What is the first step in BI process?", "Data collection", "Reporting", "Visualization", "Storage", "Data collection"),
            ("Which of these is NOT a BI tool?", "MS Word", "Power BI", "Tableau", "QlikView", "MS Word"),
            ("BI reports help managers to?", "Make better decisions", "Play games", "Write code", "Send emails", "Make better decisions"),
            ("Which component of BI is responsible for analysis?", "Analytics Layer", "Storage Layer", "Security Layer", "Network Layer", "Analytics Layer"),
            ("OLAP cubes are used for?", "Multidimensional analysis", "Flat file storage", "Simple sorting", "None", "Multidimensional analysis"),
            ("Which of these is part of BI architecture?", "Data warehouse", "Printer", "Compiler", "Cache", "Data warehouse"),
            ("What does BI improve in organizations?", "Decision accuracy", "Coding speed", "Hardware cost", "None", "Decision accuracy"),
            ("Which visualization shows parts of a whole?", "Pie chart", "Line chart", "Histogram", "Scatter plot", "Pie chart"),
            ("ETL helps to?", "Clean and load data", "Delete databases", "Encrypt servers", "Generate passwords", "Clean and load data"),
            ("Tableau is used for?", "Data visualization", "Code compilation", "Network testing", "API design", "Data visualization"),
            ("In Tableau, data blending means?", "Combining multiple sources", "Deleting rows", "Copying charts", "Filtering records", "Combining multiple sources"),
            ("Which Tableau chart shows intensity?", "Heat map", "Pie chart", "Tree map", "Line chart", "Heat map"),
            ("LOD Expressions in Tableau are used for?", "Detail-level calculations", "Color formatting", "UI design", "Data import", "Detail-level calculations"),
            ("Which Tableau feature filters data dynamically?", "Context filter", "Row ID", "Label tag", "Auto filter", "Context filter"),
            ("What is a dashboard in Tableau?", "Collection of views", "Single chart", "Database table", "Filter list", "Collection of views"),
            ("Which chart type compares categories?", "Bar chart", "Line chart", "Histogram", "Pie chart", "Bar chart"),
            ("Tableau can connect to?", "Excel, SQL", "Paint, PDF", "C++, Java", "Text editors", "Excel, SQL"),
            ("Which pane holds dimensions and measures?", "Data pane", "Format pane", "Story pane", "Color pane", "Data pane"),
            ("Which Tableau function combines fields?", "Calculated field", "Static field", "Virtual field", "Base field", "Calculated field"),
            ("Data join in Tableau combines?", "Two tables", "Charts", "Dashboards", "Filters", "Two tables"),
            ("The main output of Tableau is?", "Interactive visuals", "Static PDFs", "Plain text", "ZIP files", "Interactive visuals"),
            ("Which file stores Tableau workbook?", ".twb", ".docx", ".xlsx", ".csv", ".twb"),
            ("A story in Tableau means?", "Sequence of dashboards", "Filter name", "Data extract", "Custom field", "Sequence of dashboards"),
            ("Which type of chart shows trends over time?", "Line chart", "Pie chart", "Bar chart", "Tree map", "Line chart"),
            ("Pivoting in Tableau is used to?", "Reshape data", "Delete columns", "Merge files", "Encrypt fields", "Reshape data"),
            ("Tableau’s data extract improves?", "Performance", "Security", "Formatting", "None", "Performance"),
            ("Which chart shows hierarchical data?", "Tree map", "Bar chart", "Pie chart", "Line chart", "Tree map"),
            ("Which Tableau field stores numbers?", "Measure", "Dimension", "Label", "Tag", "Measure"),
            ("Tableau public is?", "Free platform", "Paid desktop", "SQL server", "Offline tool", "Free platform"),
            ("Power BI is mainly used for?", "Business analytics", "App development", "Image editing", "None", "Business analytics"),
            ("Power Query helps to?", "Clean data", "Encrypt data", "Compile code", "Backup files", "Clean data"),
            ("Power Pivot handles?", "Data modeling", "Text formatting", "File compression", "Web scraping", "Data modeling"),
            ("Which visual compares values?", "Bar chart", "Pie chart", "Tree map", "Text box", "Bar chart"),
            ("Power BI connects to?", "Multiple sources", "One file only", "No data", "Local cache", "Multiple sources"),
            ("Which is the formula language in Power BI?", "DAX", "SQL", "XML", "JSON", "DAX"),
            ("Which joins tables with matching data?", "Inner join", "Outer join", "Left join", "Cross join", "Inner join"),
            ("Which view builds relationships?", "Model view", "Data view", "Report view", "None", "Model view"),
            ("Which file format saves Power BI reports?", ".pbix", ".xlsx", ".csv", ".pdf", ".pbix"),
            ("Power Query Editor is used for?", "Data transformation", "Designing UI", "Encryption", "Hosting", "Data transformation"),
            ("Power BI dashboards are?", "Interactive visuals", "Static charts", "Code outputs", "Files", "Interactive visuals"),
            ("Which Power BI component loads data?", "Power Pivot", "Power View", "Power Query", "Power Map", "Power Query"),
            ("Which is a Power BI visualization?", "Card", "Table", "Bar chart", "All", "All"),
            ("Which function merges queries?", "Merge", "Append", "Combine", "Attach", "Merge"),
            ("Which feature reshapes data vertically?", "Append", "Transpose", "Reverse", "None", "Append"),
            ("Which pane contains visuals?", "Visualization pane", "Filter pane", "Model pane", "Query pane", "Visualization pane"),
            ("Which feature allows publishing?", "Power BI Service", "Excel", "GitHub", "Power Point", "Power BI Service"),
            ("Which is part of Power BI architecture?", "Dataset", "OS Kernel", "Router", "Serverless", "Dataset"),
            ("Which filter type applies to all visuals?", "Page filter", "Visual filter", "Chart filter", "Quick filter", "Page filter"),
            ("Which component helps create reports?", "Power View", "Power Shell", "Power Page", "None", "Power View"),
            ("DAX stands for?", "Data Analysis Expressions", "Data Access XML", "Dynamic API Xpress", "Data Audit Exchange", "Data Analysis Expressions"),
            ("Which DAX function aggregates data?", "SUM", "FILTER", "LEFT", "CONCATENATE", "SUM"),
            ("Fact table contains?", "Quantitative data", "Meta data", "Images", "Code", "Quantitative data"),
            ("Dimension table holds?", "Descriptive data", "Numerical data", "Code", "None", "Descriptive data"),
            ("Star schema uses?", "Central fact table", "Circular relation", "Tree relation", "None", "Central fact table"),
            ("Snowflake schema expands?", "Dimension tables", "Fact tables", "Data types", "Schemas", "Dimension tables"),
            ("KPI stands for?", "Key Performance Indicator", "Knowledge Processing Index", "Key Power Interface", "Known Parameter Input", "Key Performance Indicator"),
            ("Time intelligence functions deal with?", "Dates", "Users", "Servers", "Schemas", "Dates"),
            ("DAX FILTER function returns?", "Filtered table", "String", "Boolean", "File", "Filtered table"),
            ("DAX CALCULATE changes?", "Context", "Schema", "Format", "Output type", "Context"),
            ("Power BI relationship can be?", "One-to-many", "Many-to-one", "Circular", "Random", "One-to-many"),
            ("Fact tables connect to?", "Dimensions", "Schemas", "Logs", "Tables", "Dimensions"),
            ("Which function counts rows?", "COUNTROWS", "SUMX", "ROWCOUNT", "TOTAL", "COUNTROWS"),
            ("A DAX measure is?", "Calculated value", "Table name", "Data type", "Filter", "Calculated value"),
            ("Cross-filter direction affects?", "Data flow", "Report title", "Color", "Font", "Data flow"),
            ("Relationships define?", "Data linkage", "Security", "Format", "Encryption", "Data linkage"),
            ("DAX RELATED function returns?", "Related data", "Unrelated info", "Chart type", "File path", "Related data"),
            ("Data models use?", "Relationships", "Logs", "Tables only", "None", "Relationships"),
            ("Which chart evaluates KPIs?", "Gauge chart", "Bar chart", "Pie chart", "Area chart", "Gauge chart"),
            ("DAX expressions are used in?", "Power BI", "Tableau", "Python", "C++", "Power BI"),
            ("Power BI visuals can be?", "Bar, Pie, Line", "Only Pie", "Only Text", "Only 3D", "Bar, Pie, Line"),
            ("Drill-through allows?", "Detailed view", "Deleting data", "Merging tables", "Formatting", "Detailed view"),
            ("Row-level security restricts?", "Data access", "UI layout", "Themes", "Storage", "Data access"),
            ("Deployment pipeline helps?", "Move reports", "Encrypt data", "Add filters", "Delete logs", "Move reports"),
            ("Power BI service is?", "Cloud platform", "Offline app", "Compiler", "Editor", "Cloud platform"),
            ("Bookmarks are used for?", "Save view", "Filter data", "Join tables", "Encrypt", "Save view"),
            ("Selection pane controls?", "Visibility", "Security", "Data type", "Layout", "Visibility"),
            ("Matrix visual is similar to?", "Pivot table", "Pie chart", "Tree map", "Gauge", "Pivot table"),
            ("Table visual shows?", "Raw data", "Images", "Audio", "Icons", "Raw data"),
            ("Power BI workspace is for?", "Collaboration", "Coding", "Encryption", "Designing", "Collaboration"),
            ("Drill-down reveals?", "Lower-level data", "Summaries", "Charts only", "Logs", "Lower-level data"),
            ("Filters help in?", "Refining data", "Deleting reports", "Adding users", "Testing UI", "Refining data"),
            ("Power View supports?", "Visual reports", "Network tests", "Encryption", "Schema building", "Visual reports"),
            ("RLS uses?", "User roles", "Color tags", "Server logs", "None", "User roles"),
            ("Power BI mobile app is for?", "Viewing reports", "Editing code", "Encrypting data", "Schema design", "Viewing reports"),
            ("KPI visual displays?", "Performance metric", "Data model", "Schema", "Color filter", "Performance metric"),
            ("Dashboard tiles are?", "Pinned visuals", "Logs", "Pages", "Tables", "Pinned visuals"),
            ("Publishing sends reports to?", "Cloud service", "Printer", "Excel", "Drive", "Cloud service"),
            ("Which file type is Power BI dataset?", ".pbix", ".txt", ".csv", ".docx", ".pbix"),
            ("Power BI reports can be shared via?", "Links", "Emails only", "Pen drives", "QR codes", "Links"),
        ]


for q in questions_data:
    text, opt_a, opt_b, opt_c, opt_d, correct_text = q

    # Determine correct answer letter (A, B, C, or D)
    options = [opt_a, opt_b, opt_c, opt_d]
    correct_letter = None
    for i, option in enumerate(options):
        if option == correct_text:
            correct_letter = chr(65 + i)  # 65 = 'A', 66 = 'B', etc.
            break

    if correct_letter is None:
        print(f"⚠️ Warning: Could not match correct answer for question: {text}")
        continue

    IOTQuestion.objects.create(
        text=text,
        option_a=opt_a,
        option_b=opt_b,
        option_c=opt_c,
        option_d=opt_d,
        correct_answer=correct_letter,  # Must be 'A', 'B', 'C', or 'D'
        marks=1  # All your questions are 1-mark
        # image_url is optional and defaults to None
    )

print("✅ All questions added successfully!")