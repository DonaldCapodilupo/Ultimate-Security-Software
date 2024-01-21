const business_name = "Capodilupo Investigation's";
const address = "123 Main St,\n Disney Land, FL 90210";


function create_Business_Header() {
    let header_div = document.getElementById("Business Header");
    if (header_div.textContent === "") {
        console.log(header_div);
        header_div.innerHTML +=
            "<h3>" + business_name + "</h3>" +
            "<h5>" + address + "</h5>";
    }

}

function get_Current_Time() {
    const date = new Date();

    let day = date.getDate();
    let month = date.getMonth() + 1;
    let year = date.getFullYear();

    if (month < 10) month = "0" + month;
    if (day < 10) day = "0" + day;

    // This arrangement can be altered based on how we want the date's format to appear.
    let today = year + "-" + month + "-" + day;
    console.log(today); // "17-6-2022"

    return today;
}


function setup_BOLO_HTML() {
    const bolo_details = {
        "BOLO Person Details": {
            "Name": "text",
            "Alias/AKA": "text",
            "DOB": "text",
            "Sex": "text",
            "Race": "text",
            "Ethnicity": "text",
            "Height": "text",
            "Weight": "text",
            "Hair": "text",
            "Eyes": "text",
            "DLB": "text",
            "SSN": "text",
            "LKA": "text",
            "Know Associates": "text",
        },
        "BOLO Car Details": {
            "Make": "text",
            "Model": "text",
            "Color": "text",
            "Last Known Location": "text",
            "Notable Markings": "text",
            "Date Last Seen": "text",
            "Considered Dangerous": "text",
            "Owner": "text",
            "VIN": "text",
        }


    };

    for (let [div_to_fill, table_dict] of Object.entries(bolo_details)) {
        let new_table = new Table_Creator(div_to_fill, table_dict);
    }
}


function case_Number_Generator() {
    let customer_name = document.getElementById("Customer Name").value;
    let case_type = document.getElementById("Investigation Type").value;

    case_number = customer_name.slice(0, 3) + "-" + case_type + "-001";

    console.log(case_number);

    document.getElementById("generated_case_number").value = case_number;


}

function setup_Case_Number_Generator() {
    let customer_name_field = document.getElementById("Returning Customer Name");


    customer_name_field.addEventListener("input", function (event) {

        case_Number_Generator();

    });


}

