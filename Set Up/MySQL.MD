## <b>Steps to Create the Database</b>
<hr><br>

#### Perform the following actions in your MySQL Command Line:
<ol>
    <li>Create a new database having name as <b>"Bank"</b></li>
    <li>Create a new table <b>"Customer"</b> having the following attributes:
        <ul style = "list-style-type: disc">
            <li>cust_id int primary key auto_increment</li>
            <li>name varchar(50)</li>
            <li>DOB varchar(15)</li>
        </ul>
        Now, to set the auto_increment from the number 100, run the following command: <b>ALTER TABLE Customer AUTO_INCREMENT = 100;</b>
    </li>
    <li>Create a new table <b>"Branch"</b> having the following attributes:
        <ul style = "list-style-type: disc">
            <li>cust_id int primary key auto_increment</li>
            <li>name varchar(50)</li>
            <li>DOB varchar(15)</li>
        </ul>

</ol>