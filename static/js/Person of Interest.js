/*jshint esversion: 6 */
/* global console*/
/* use strict*/

const
    table_structure = {
        "Basic Details":
            {
                "First Name": "text",
                "Last Name": "text",
                "Middle Name": "text",
                "Home Address": "text",
                "Town": "text",
                "State": ['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY'],
                "Zip": "number",
                "Marital Status":["Single","In a Relationship", "Married", "Divorced", "Infidelity"]
            },
        "Contact Info":
            {
                "Phone Number": "text",
                "Email": "text",
            },

        "Identifying Info":
            {
                "Height": "text",
                "Weight": "number",
                "Hair Color": ['Black', 'Brown', 'Blonde', 'Red', 'Gray', 'White', 'Auburn', 'Chestnut', 'Strawberry Blonde', 'Dirty Blonde', 'Platinum Blonde', 'Silver', 'Salt and Pepper', 'Blue', 'Green', 'Pink', 'Purple', 'Turquoise', 'Rainbow', 'Ombre', 'Balayage', 'Highlights', 'Lowlights', 'Natural', 'Bald', 'Balding', 'Shaved', 'Salt and Pepper',],
                "Eye Color": ['Brown', 'Blue', 'Green', 'Hazel', 'Amber', 'Gray', 'Black', 'Red', 'Violet',],
                "Skin Color": ['African', 'Asian', 'Caucasian', 'Hispanic', 'Latino', 'Native American', 'Pacific Islander', 'Middle Eastern', 'Mixed',],
                "Scars - Marks - Tattoos": "text",
                "Shoe Size": "text",
            },

        "Employment Info":
            {
                "Employer": "text",
                "Employer Address": "text",
                "Length of Employment": "text",
                "Job Title": "text",
                "Work Phone": "text",
                "Prior Military Experience": "text",

            },

        "Vehicle Info":
            {
                "Year": "number",
                "Make": "text",
                "Model": "text",
                "License Plate": "text",
                "VIN": "text",
            },

        "Criminal Intentions":
            {
                "Prior Arrests":"text",
                "Own Firearm":"text",
                "Prior Felonies":"text",
                "Martial Arts or Combat Experience":"text",
                "Currently Under Investigation":["No","Unknown","Yes"],
                "Outstanding Warrants" : "text"

            }

    };


class Table_Creator {
    constructor(title, question_and_input_dict) {

        this.title = title;
        this.question_and_input_dict = question_and_input_dict;


        //Find the div within the HTML File
        this.div = title.replaceAll(" ", "-") + "-Table";
        this.div_to_be_filled = document.getElementById(this.div);

        this.table_name = title + ' Table';


    }

    create_Table_Header() {
        console.log(this.div_to_be_filled);
        this.div_to_be_filled.innerHTML +=
            '<div class="Input-Table">' +
            '   <div class="Title-Row">' +
            '       <p>' + this.title + '</p>' +
            '   </div>' +
            '   <table id="' + this.table_name + '"> </table>' +
            '</div>';
    }


    create_Table_Body() {
        for (let [label, input_type] of Object.entries(this.question_and_input_dict)) {

            let table_to_fill = document.getElementById(this.table_name);
            let backend_label_text = this.title + ' ' + label;
            let row_to_be_fill = backend_label_text + '-Row';

            table_to_fill.innerHTML +=
                '<tr id="' + row_to_be_fill + '" class="row mb-1">' +
                '<td><label for="' + backend_label_text + '" class="text_label">' + label + ': </label></td>' +
                '</tr>';

            let row_to_fill = document.getElementById(row_to_be_fill);


            if (input_type === "number") {
                row_to_fill.innerHTML +=
                    '<td><input name="' + backend_label_text + '" class="form-control" type="number" step="0.01" id="' + backend_label_text + '"  value="' + input_type + '"></td></tr>';
            } else if (input_type === "text") {
                row_to_fill.innerHTML +=
                    '<td><input name="' + backend_label_text + '" class="form-control" type=' + input_type + ' id="' + backend_label_text + '"></td></tr>';
            } else if (input_type === "time") {
                row_to_fill.innerHTML +=
                    '<td><input name="' + backend_label_text + '" class="form-control" type=' + input_type + ' id="' + backend_label_text + '" value="07:00"></td></tr>';

            } else if (input_type === "label") {
                row_to_fill.innerHTML +=
                    '<td><span  id="Output ' + backend_label_text + '">0.00</span></td></tr>';
            } else if (input_type.constructor === Array) {
                row_to_fill.innerHTML +=

                    '<select name="' + backend_label_text + '" id="' + backend_label_text + '"> </select>';


                for (const variable of input_type) {
                    console.log(variable + " is the variable.");
                    document.getElementById(backend_label_text).innerHTML +=
                        '<option id="' + variable + '">' + variable + '</option>';

                }
                row_to_fill.innerHTML += '</tr>';


            }

        }


    }


    create_Complex_Table() {


        let table_to_fill = document.getElementById(this.table_name);

        //let row_to_be_fill = backend_label_text + '-Row'


        table_to_fill.innerHTML +=
            '<tr>' +
            '<th></th>' +
            '<th>Today</th>' +
            '<th>Yesterday</th>' +
            '<th>Used</th>' +
            '</tr>';


        for (let [question, dict_of_stuff] of Object.entries(this.question_and_input_dict)) {
            for (let [test, input_type] of Object.entries(dict_of_stuff)) {

                console.log(test);

                let backend_label_text = this.title + ' ' + test;

                console.log("backend label text: " + backend_label_text);

                table_to_fill.innerHTML +=
                    '<td><p>' + test + ':</p></td>' +
                    '<td><input class="form-control" type="number" step="0.01" id="' + backend_label_text + ' Today" value="' + input_type[0] + '"></td>' +
                    '<td><input class="form-control" type="number" step="0.01" id="' + backend_label_text + ' Yesterday" value="' + input_type + '"></td>' +
                    '<td><input class="form-control" type="number" step="0.01" id="' + backend_label_text + ' Used" value="' + input_type + '"></td>';


            }
            break;


        }


    }
}


function populateLists() {
    const lists_to_populate = [eye_color, hair_color, marital_status, politics, gender];
    const div_ids = ["eye_color", "hair_color", "marital_status", "political_affiliation", "gender"];

    let car_data = JSON.parse(json);

    for (let list_to_populate = 0; list_to_populate < lists_to_populate.length; list_to_populate++) {

        console.log(lists_to_populate[list_to_populate]);

        for (let specific_item = 0; specific_item < lists_to_populate[list_to_populate].length; specific_item++) {
            console.log(lists_to_populate[list_to_populate][specific_item]);


            var opt = lists_to_populate[list_to_populate][specific_item];
            var el = document.createElement("option");
            el.textContent = opt;
            el.value = opt;
            console.log(div_ids[list_to_populate]);

            try{
                document.getElementById(div_ids[list_to_populate]).appendChild(el);
            }catch (TypeError){}
        }
    }

}


function showUserImage() {
    const img = document.getElementById('preview');
    const input = document.getElementById('user_img');
    input.onchange = function (ev) {
        const file = ev.target.files[0]; // get the file
        const blobURL = URL.createObjectURL(file);
        img.src = blobURL;
    };
}






function setUpHTML() {

    for (let [title, question_and_prompt_dict] of Object.entries(table_structure)) {


        let new_table = new Table_Creator(title, question_and_prompt_dict);

        new_table.create_Table_Header();
        new_table.create_Table_Body();


        /*if ("Plant Chemicals" === title || "Comag Chemicals" === title) {
            new_table.create_Complex_Table();

        } else {
            new_table.create_Table_Body();
        }

         */


    }
}