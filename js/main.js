function correctElements(){
    console.log($(window).width());
    if ($(window).width() < 1340){
        var itemButtonParents = document.getElementById('item-buttons');
        var ingButtonParents = document.getElementById('ing-buttons');

        document.getElementById("item-export").classList.add("col","py-3", "text-center")
        document.getElementById("item-export").classList.add("col","py-3", "text-center")
        document.getElementById("item-import").classList.remove("d-inline-block", "px-3")
        document.getElementById("item-import").classList.remove("d-inline-block", "pl-3")

        document.getElementById("ing-export").classList.add("col","py-2", "px-4", "text-center")
        document.getElementById("ing-export").classList.remove("d-inline-block")

        itemButtonParents.appendChild(document.getElementById("item-import"))
        itemButtonParents.appendChild(document.getElementById("item-export"))

        ingButtonParents.appendChild(document.getElementById("ing-export"))
    }else{
        var itemButtonParents = document.getElementById('item-div');
        var ingButtonParents = document.getElementById('ing-div');

        document.getElementById("item-export").classList.remove("col","py-3", "text-center")
        document.getElementById("item-export").classList.remove("col","py-3", "text-center")
        document.getElementById("item-import").classList.add("d-inline-block", "px-3", "text-right")
        document.getElementById("item-import").classList.add("d-inline-block", "pl-3", "text-right")

        document.getElementById("ing-export").classList.remove("col","py-2", "px-4", "text-center")
        document.getElementById("ing-export").classList.add("d-inline-block")

        itemButtonParents.appendChild(document.getElementById("item-export"))
        itemButtonParents.appendChild(document.getElementById("item-import"))

        ingButtonParents.appendChild(document.getElementById("ing-export"))
    }

    if ($(window).width() < 1000){
        document.getElementById("item-row").appendChild(document.getElementById("item-col"))
        document.getElementById("ing-row").appendChild(document.getElementById("ing-col"))
    }else{
        document.getElementById("search-row").appendChild(document.getElementById("item-col"))
        document.getElementById("search-row").appendChild(document.getElementById("ing-col"))
    }
}

function turn_off_warnings(){
    $.ajax({
        type: "GET",
        url: '/show_warning?set=hide',
        success: function(response){
            show_warning = (response === "True")
            document.getElementById('warning-toggle').setAttribute('onclick','turn_on_warnings()')
            document.getElementById('warning-toggle').setAttribute('class','toggle-off')
            document.getElementById('warning-toggle').innerText = "Turn on warnings"
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Something went wrong when contacting the server.',
                showConfirmButton: false,
                timer: 2000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });
}

function turn_on_warnings(){
    $.ajax({
        type: "GET",
        url: '/show_warning?set=show',
        success: function(response){
            show_warning = (response === "True")
            document.getElementById('warning-toggle').setAttribute('onclick','turn_off_warnings()')
            document.getElementById('warning-toggle').setAttribute('class','toggle-on')
            document.getElementById('warning-toggle').innerText = "Turn off warnings"
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Something went wrong when contacting the server.',
                showConfirmButton: false,
                timer: 2000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });
}

function clear_search() {
    if(document.getElementById("search").value === ""){
        Swal.fire({
            position: 'top',
            icon: 'warning',
            title: 'Search box is already clear! :)',
            showConfirmButton: false,
            timer: 2000,
            backdrop: false,
            toast: true,
            customClass: {
                border: '5px solid black'
            }
        })
    }else{
        document.getElementById("search").value = "";
    }
    doneSearchTyping();
}

function exportItems() {
    /* Get the text field */
    var copyElement = document.getElementById("copyboard");
    var copyText = "";

    $.ajax({
        type: "GET",
        url: '/get?type=items',
        success: function (response) {
            response = JSON.parse(response);
            items = response['items'];
            for (var i = 0; i < items.length; i++) {
                amount = items[i].amount
                if (amount > 64) {
                    multiple = Math.floor(amount / 64.0);
                    extra = amount % 64;
                    amount = multiple + " x 64 + " + extra;
                } else {
                    amount = amount + "";
                }

                copyText += items[i].data.title + " [" + amount + "]\n"
            }

            copyElement.innerText = copyText

            if (document.body.createTextRange) {
                range = document.body.createTextRange();
                range.moveToElementText(copyElement);
                range.select();
            } else if (window.getSelection) {
                selection = window.getSelection();
                range = document.createRange();
                range.selectNodeContents(copyElement);
                selection.removeAllRanges();
                selection.addRange(range);
            }

            /* Copy the text inside the text field */
            document.execCommand("copy");

            copyElement.innerText = ""

            Swal.fire({
                position: 'top',
                icon: 'success',
                title: 'Copied items to clipboard!',
                showConfirmButton: false,
                timer: 2000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Something went wrong when contacting the server.',
                showConfirmButton: false,
                timer: 2000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });


}

function exportIngredients() {
    /* Get the text field */
    var copyElement = document.getElementById("copyboard");
    var copyText = "";

    $.ajax({
        type: "GET",
        url: '/get?type=ingredients',
        success: function (response) {
            response = JSON.parse(response);
            ingredients = response['ingredients'];
            for (var i = 0; i < ingredients.length; i++) {
                amount = ingredients[i].amount;
                if (amount > 64) {
                    multiple = Math.floor(amount / 64.0);
                    extra = amount % 64;
                    amount = multiple + " x 64 + " + extra;
                } else {
                    amount = amount + "";
                }

                copyText += ingredients[i].data.title + " [" + amount + "]\n"
            }

            copyElement.innerText = copyText

            if (document.body.createTextRange) {
                range = document.body.createTextRange();
                range.moveToElementText(copyElement);
                range.select();
            } else if (window.getSelection) {
                selection = window.getSelection();
                range = document.createRange();
                range.selectNodeContents(copyElement);
                selection.removeAllRanges();
                selection.addRange(range);
            }

            /* Copy the text inside the text field */
            document.execCommand("copy");

            copyElement.innerText = ""

            Swal.fire({
                position: 'top',
                icon: 'success',
                title: 'Copied ingredients to clipboard!',
                showConfirmButton: false,
                timer: 2000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Something went wrong when contacting the server.',
                showConfirmButton: false,
                timer: 2000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });
}

show_warning = true

$(document).ready(function () {
    $.ajax({
        type: "GET",
        url: '/show_warning',
        success: function(response){
            show_warning = (response === "True")
            if(show_warning){
                turn_on_warnings()
            }else{
                turn_off_warnings()
            }
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Something went wrong when contacting the server.',
                showConfirmButton: false,
                timer: 2000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });

    $('[data-toggle="tooltip"]').tooltip();
    anime.set(".slide",{
        opacity: 0,
        translateX: 0
    });

    setSearchPreviewOpacity()
    setHover()
    $.ajax({
        type: "GET",
        url: '/get',
        success: function (response) {
            response = JSON.parse(response);
            render_items_and_ingredients(response['items'], response['ingredients']);
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Something went wrong when contacting the server.',
                showConfirmButton: false,
                timer: 2000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });
    $.ajax({
        type: "GET",
        url: '/last_search',
        success: function (response) {
            document.getElementById("search").value = response;
            console.log(response)
            doneSearchTyping();
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Something went wrong when contacting the server.',
                showConfirmButton: false,
                timer: 2000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });
    correctElements()
    $.ajax({
        type: "GET",
        url: '/version',
        success: function(response){
            $("#version").attr("href","https://github.com/FrankWhoee/Aedifex/releases/tag/v" + response);
            $("#version").text("Aedifex v" + response);
        }
    });


});

function refresh(){
    $.ajax({
        type: "GET",
        url: '/get',
        success: function (response) {
            response = JSON.parse(response);
            render_items_and_ingredients(response['items'], response['ingredients']);
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Something went wrong when contacting the server.',
                showConfirmButton: false,
                timer: 2000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });
}

function cata(){
    $.ajax({
        type: "GET",
        url: '/cata',
        success: function (response) {
            response = JSON.parse(response);
            render_items_and_ingredients(response['items'], response['ingredients']);
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Something went wrong when contacting the server.',
                showConfirmButton: false,
                timer: 2000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });
}

function ana(){
    $.ajax({
        type: "GET",
        url: '/ana',
        success: function (response, textStatus, xhr) {
            console.log(xhr.status)
            if (xhr.status === 204){
                Swal.fire({
                    position: 'top',
                    icon: 'warning',
                    title: 'You can not tier up an original list!',
                    showConfirmButton: false,
                    timer: 2000,
                    toast: true,
                    customClass: {
                        border: '5px solid black'
                    }
                })
            }else{
                response = JSON.parse(response);
                render_items_and_ingredients(response['items'], response['ingredients']);
            }
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Something went wrong when contacting the server.',
                showConfirmButton: false,
                timer: 2000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });
}

function ana_complete(){
    $.ajax({
        type: "GET",
        url: '/ana_complete',
        success: function (response) {
            response = JSON.parse(response);
            render_items_and_ingredients(response['items'], response['ingredients']);
            Swal.fire({
                position: 'top',
                icon: 'success',
                title: 'List has been reverted completely.',
                showConfirmButton: false,
                timer: 2000,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Something went wrong when contacting the server.',
                showConfirmButton: false,
                timer: 2000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });
}


function setSearchPreviewOpacity(){
    items = document.getElementsByClassName("add-hover")
    for (var i = 0; i < items.length; i++) {
        items[i].style.opacity = calculateScaleTransform(items[i])
    }
}


function calculateScaleTransform(object) {
    elementY = object.getBoundingClientRect().top;
    elementHeight = $(object).height();
    topbound = document.getElementById("search-preview").getBoundingClientRect().top;
    lowbound = document.getElementById("search-preview").getBoundingClientRect().bottom;
    if (elementY < topbound || elementY > lowbound) {
        return 0
    } else if (elementY < topbound + elementHeight) {
        return Math.abs(((topbound - elementY) / elementHeight));
    } else if (elementY > lowbound - elementHeight) {
        return Math.abs(((elementY - lowbound) / elementHeight));
    } else {
        return 1;
    }
}

function getRemoveTarget(object){
    possibleElements = $(object).children()[0].children;

    for (i = 0; i < possibleElements.length; i++) {
        if (possibleElements[i].nodeType !== 3 && possibleElements[i].className.includes("slide")) {
            return possibleElements[i]
        }
    }

}

function getAddTarget(object) {
    possibleElements = $(object).children()[0].children;

    for (i = 0; i < possibleElements.length; i++) {
        if (possibleElements[i].nodeType !== 3 && possibleElements[i].className.includes("slide")) {
            return $(possibleElements[i])
        }
    }

}

$(window).scroll(function () {
    setSearchPreviewOpacity()
});

$('#search-preview').scroll(function () {
    setSearchPreviewOpacity()
});

function setHover(){


    $(".add-hover").hover(function () {
        animeTarget = getRemoveTarget(this);
        anime({
            targets: animeTarget,
            opacity: 1,
            translateX: 25,
        });
    }, function () {
        animeTarget = getRemoveTarget(this);
        anime({
            targets: animeTarget,
            opacity: 0,
            translateX: 0,
        });
    });

    $(".remove-hover").hover(function () {
        animeTarget = getRemoveTarget(this);
        anime({
            targets: animeTarget,
            opacity: 1,
            translateX: 40,
        });
    }, function () {
        animeTarget = getRemoveTarget(this);
        anime({
            targets: animeTarget,
            opacity: 0,
            translateX: 0,
        });
    });

    $('.add-hover').on('mouseover', function () {
        var $menuItem = $(this);
        var $submenuWrapper = getAddTarget(this);

        repeater = setInterval(function () {


            // grab the menu item's position relative to its positioned parent
            var menuItemPos = $menuItem.position();

            // place the submenu in the correct position relevant to the menu item
            $submenuWrapper.css({
                top: menuItemPos.top + $submenuWrapper.height() / 1.5
            });
        }, 100);
    });

    $('add-hover').on('mouseout', function () {
        clearInterval(repeater)
    })

    prevKeyup = '-1'

    $('.item-amount-edit').keydown(function (e) {
        var code = (e.which);
        console.log(code)
        if(!(code <= 90 && code >= 65)){
            prevKeyup = code;
        }
    });

    $('.item-amount-edit').keyup(function (e) {
        var code = (e.which);
        console.log("prev" + prevKeyup + " curr"+code)
        if(prevKeyup === 17 && code === 65){
            return;
        }
        // do nothing if it's an arrow key
        if(code === 37 || code === 38 || code === 39 || code === 40 || code === 17) {
            return;
        }
        clearTimeout(itemTypingTimer);
        itemTypingTimer = setTimeout(doneItemTyping, doneTypingInterval);
    });

    function doneItemTyping() {
        activeId = document.activeElement.id;
        items = document.getElementsByClassName("item-amount-edit");
        payload = "";
        amounts = []
        for (var i = 0; i < items.length; i++) {
            item = items[i].id.substring(0, items[i].id.indexOf("_item_input")).replace("_", " ").replace(".json", "");

            amount = parseInt(items[i].value);
            if (items[i].value === "") {
                amount = 1
            } else if (!amount) {
                Swal.fire({
                    position: 'top',
                    icon: 'error',
                    title: 'Bad number input. Are you sure you\'re entering an integer?',
                    showConfirmButton: false,
                    timer: 2000,
                    backdrop: false,
                    toast: true,
                    customClass: {
                        border: '5px solid black'
                    }
                })

                var basicTimeline = anime.timeline({
                    targets: items[i]
                });

                basicTimeline.add({
                    borderColor: ['rgb(0,0,0)', 'rgb(255,0,0)'],
                    duration: 500,
                    backgroundColor: ['rgb(255,255,255)', 'rgb(255,0,0)'],
                    easing: 'easeInOutExpo'
                }).add({
                    backgroundColor: ['rgb(255,0,0)', 'rgb(255,255,255)'],
                    duration: 2000,
                    easing: 'easeInOutExpo'
                }).add({
                    borderColor: ['rgb(255,0,0)', 'rgb(0,0,0)'],
                    duration: 500,
                    easing: 'easeInOutExpo'
                });
                return
            }


            if (amount > 64) {
                multiple = Math.floor(amount / 64.0);
                extra = amount % 64;
                amount = multiple + " x 64 + " + extra;
            } else {
                amount = amount + "";
            }
            amounts.push(amount)
            payload += item + " [" + amount + "]\n"
        }

        show_history_erase_warning(function(){
                $.ajax({
                    type: "POST",
                    url: '/import',
                    data: JSON.stringify({"data": payload, "replace": true}),
                    success: function (response) {
                        response = JSON.parse(response)
                        render_items_and_ingredients(response['items'], response['ingredients'])
                        document.getElementById(activeId).focus()
                        val = document.getElementById(activeId).value
                        document.getElementById(activeId).value = ''
                        document.getElementById(activeId).value = val
                    },
                    error: function (response) {
                        Swal.fire({
                            position: 'top',
                            icon: 'error',
                            title: 'Something went wrong when contacting the server.',
                            showConfirmButton: false,
                            timer: 2000,
                            backdrop: false,
                            toast: true,
                            customClass: {
                                border: '5px solid black'
                            }
                        })
                    }
                });
            },warning="Changing this amount will erase your history. You won't be able to undo your breakdown."
            ,confirmation="Yes, change the amount!", cancelfn=function(){
                $.ajax({
                    type: "GET",
                    url: '/get',
                    success: function (response) {
                        response = JSON.parse(response)
                        render_items_and_ingredients(response['items'], response['ingredients'])
                    },
                    error: function (response) {
                        Swal.fire({
                            position: 'top',
                            icon: 'error',
                            title: 'Something went wrong when contacting the server.',
                            showConfirmButton: false,
                            timer: 2000,
                            backdrop: false,
                            toast: true,
                            customClass: {
                                border: '5px solid black'
                            }
                        })
                    }
                });
            }
        )


    }
}


/*

<br>
* */

function remove_item(object){
    show_history_erase_warning(fn=function(){
            $.ajax({
                type: "GET",
                url: '/remove?item=' + $(object).attr('id'),
                success: function (response) {
                    response = JSON.parse(response)
                    render_items_and_ingredients(response['items'], response['ingredients'])
                },
                error: function (response) {
                    Swal.fire({
                        position: 'top',
                        icon: 'error',
                        title: 'Something went wrong when contacting the server.',
                        showConfirmButton: false,
                        timer: 2000,
                        backdrop: false,
                        toast: true,
                        customClass: {
                            border: '5px solid black'
                        }
                    })
                }
            });
        }, warning="Deleting this item will erase your history. You won't be able to undo your breakdown."
        , confirmation="Yes, delete this item!")

}

function delete_all(){
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.value) {
            $.ajax({
                type: "GET",
                url: '/delete_all',
                success: function(response){
                    $('#items').get(0).innerHTML = '';
                    $('#ingredients').get(0).innerHTML = '';
                },
                error: function (response) {
                    Swal.fire({
                        position: 'top',
                        icon: 'error',
                        title: 'Something went wrong when contacting the server.',
                        showConfirmButton: false,
                        timer: 2000,
                        backdrop: false,
                        toast: true,
                        customClass: {
                            border: '5px solid black'
                        }
                    })
                }
            })
        }
    })
}

async function import_items() {
    const { value: formValues } = await Swal.fire({
        title: "Import a list of items.",
        html:
            '<div id="swal2-content" class="swal2-html-container" style="display: block;">Use the format {ITEM} [AMOUNT] for each item. Each item should be in seperate lines</div>' +
            '<textarea autocapitalize="off" id="swal2-textarea" class="swal2-textarea" placeholder="Oak Wood [6 x 64 + 36]\n' +
            'Redstone [64]\n' +
            'Repeater [2]\n' +
            'Sticky Piston [12]" style="display: flex;" spellcheck="false"></textarea>' +
            '<div class="row justify-content-center">' +
                '<div class="col-sm-1">' +
                    '<input style="display: inline-block;" type="checkbox" value="1" id="swal2-checkbox">' +
                '</div>' +
                '<div class="col-sm-auto">' +
                    '<span class="swal2-label" style="display: inline-block;">Replace current items?</span>' +
                '</div class="col">' +
            '</div>',
        showCancelButton: true,
        confirmButtonText: 'Import',
        showLoaderOnConfirm: true,
        preConfirm: () => {
            return [
                document.getElementById('swal2-textarea').value,
                document.getElementById('swal2-checkbox').checked
            ]

        },
        allowOutsideClick: () => !Swal.isLoading()
    })

    if (formValues) {
        $.ajax({
            type: "POST",
            url: '/import',
            data: JSON.stringify({"data":formValues[0],"replace":formValues[1]}),
            success: function (response) {
                response = JSON.parse(response)
                render_items_and_ingredients(response['items'], response['ingredients'])
            },
            error: function (response) {
                Swal.fire({
                    position: 'top',
                    icon: 'error',
                    title: 'Something went wrong when contacting the server.',
                    showConfirmButton: false,
                    timer: 2000,
                    backdrop: false,
                    toast: true,
                    customClass: {
                        border: '5px solid black'
                    }
                })
            }
        }).then(function(){
            Swal.fire({
                position: 'top',
                icon: 'success',
                title: 'List was succesfully imported',
                showConfirmButton: false,
                timer: 2000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        })
    }
}

function render_items_and_ingredients(items, ingredients) {

    $('#items').get(0).innerHTML = '';
    $('#ingredients').get(0).innerHTML = '';
    for(i = 0; i < items.length; i++){
        var card = document.createElement('div');
        data = items[i].data;
        amount = items[i].amount;
        path = data.path;
        icon = data.icon === "" ? "?" : '<img src="'+data.icon+'" style="height: 25px">\n';
        title = data.title;
        id = data.id;

        card.innerHTML = '<div class="card-white remove-hover">\n' +
            '        <div class="row">\n' +
            '            <div class="col-sm-2 center-block">\n' +
            '                 ' + icon +
            '            </div>\n' +
            '            <div class="col-6 text-center">\n' +
            '                '+title+'\n' +
            '            </div>\n' +
            '<div class="col amount_input">\n' +
            '                            <input class="px-3 text-center item-amount-edit" type="text" id="' + id + '_item_input' + '" value="' + amount + '" placeholder="1" name="fname">\n' +
            '            </div>' +
            '            <div class="col-sm-1 slide exit-icon">\n' +
            '                                <a href="#" id="' + id + '" onclick="remove_item(this)"><img src="assets/exit.png" style="height: 25px"></a>\n' +
            '            </div>'+
            '        </div>\n' +
            '    </div>'

        $('#items').get(0).appendChild(card)
        $('#items').get(0).appendChild(document.createElement("br"))
    }

    for(i = 0; i < ingredients.length; i++){
        var card = document.createElement('div');
        data = ingredients[i].data;
        amount = ingredients[i].amount;
        path = data.path;
        icon = data.icon === "" ? "?" : '<img src="'+data.icon+'" style="height: 25px">\n';
        title = data.title;

        card.innerHTML = '<div class="card-white remove-hover">\n' +
            '        <div class="row">\n' +
            '            <div class="col-sm-2 center-block">\n' +
            '                 ' + icon +
            '            </div>\n' +
            '            <div class="col-6 text-center">\n' +
            '                '+title+'\n' +
            '            </div>\n' +
            '            <div class="col text-center">\n' +
            '                                '+amount+'\n' +
            '                            </div>' +
            '            </div>' +
            '        </div>\n' +
            '    </div>'

        $('#ingredients').get(0).appendChild(card)
        $('#ingredients').get(0).appendChild(document.createElement("br"))
    }
    setHover()
    anime.set('.exit-icon', {
        opacity: 0,
        translateX: 0,
    });
}

function show_history_erase_warning(fn, warning="Completing this action will erase your history. you won't be able to undo your breakdown.", confirmation="Yes, do it!", cancelfn=function (){}){
    if(show_warning){
        $.ajax({
            type: "GET",
            url: '/tier',
            success: function(response){
                if(parseInt(response) > 0){
                    Swal.fire({
                        title: 'Are you sure?',
                        text: warning,
                        icon: 'warning',
                        showCancelButton: true,
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: confirmation
                    }).then((result) => {
                        if (result.value) {
                            fn()
                            return true
                        }else{
                            cancelfn()
                            return false
                        }
                    })
                }else{
                    fn()
                    return true
                }
            },
            error: function (response) {
                cancelfn()
                Swal.fire({
                    position: 'top',
                    icon: 'error',
                    title: 'Something went wrong when contacting the server.',
                    showConfirmButton: false,
                    timer: 2000,
                    backdrop: false,
                    toast: true,
                    customClass: {
                        border: '5px solid black'
                    }
                })
                return false
            }
        });
    }else{
        fn()
    }
}


function add_item(object){
    amount = document.getElementById($(object).attr('id') + "_input").value;
    show_history_erase_warning(function (){
            $.ajax({
                type: "GET",
                url: '/add?item=' + $(object).attr('id') + '&amount=' + amount,
                success: function(response){
                    response = JSON.parse(response)
                    render_items_and_ingredients(response['items'], response['ingredients'])
                },
                error: function (response) {
                    Swal.fire({
                        position: 'top',
                        icon: 'error',
                        title: 'Something went wrong when contacting the server.',
                        showConfirmButton: false,
                        timer: 2000,
                        backdrop: false,
                        toast: true,
                        customClass: {
                            border: '5px solid black'
                        }
                    })
                }
            });
        },
        warning="Adding this item will erase your history. You won't be able to undo your breakdown.",
        confirmation="Yes, add this item!"
    )
}

//setup before functions
var searchTypingTimer;                //timer identifier
var itemTypingTimer;                //timer identifier
var doneTypingInterval = 150;  //time in ms (5 seconds)

//on keyup, start the countdown
$('#search').keyup(function () {
    clearTimeout(searchTypingTimer);
    if ($('#search').val()) {
        searchTypingTimer = setTimeout(doneSearchTyping, doneTypingInterval);
    }
});

window.onresize = function(event) {
    correctElements()
};

//user is "finished typing," do something
function doneSearchTyping() {
    var inputVal = document.getElementById("search").value;
    console.log('/search?term=' + inputVal)
    $.ajax({
        type: "GET",
        url: '/search?term=' + inputVal,
        success: function(response){
            $('#search-preview').get(0).innerHTML = '';
            response = JSON.parse(response);
            for(i = 0; i < response.length; i++){
                var card = document.createElement('div');

                icon = response[i].icon == "" ? "?" : '<img src="'+response[i].icon+'" style="height: 25px">\n'

                card.innerHTML = '<div class="card-white add-hover">\n' +
                    '        <div class="row">\n' +
                    '            <div class="col-sm-2 center-block">\n' +
                    '                 ' + icon +
                    '            </div>\n' +
                    '            <div class="col-6 text-center">\n' +
                    '                '+response[i].title+'\n' +
                    '            </div>\n' +
                    '<div class="col amount_input">\n' +
                    '                            <input class="px-3 text-center" type="text" id="' + response[i].path + '_input' + '" placeholder="1" name="fname" style="border-radius: 20px; border: black 1px solid; width: 100%">\n' +
                    '            </div>' +
                    '            <div class="col-sm-1 slide overflow-trick">\n' +
                    '                <a href="#" id="'+response[i].path+'" onclick="add_item(this)"><img src="assets/rightarrow.png" style="height: 25px;"></a>\n' +
                    '            </div>\n' +
                    '        </div>\n' +
                    '    </div>'

                $('#search-preview').get(0).appendChild(card)
                $('#search-preview').get(0).appendChild(document.createElement("br"))
            }

            setSearchPreviewOpacity()
            setHover()
            anime.set('.overflow-trick', {
                opacity: 0,
                translateX: 0,
            });
        },
        error: function (response) {
            Swal.fire({
                position: 'top',
                icon: 'error',
                title: 'Something went wrong when contacting the server.',
                showConfirmButton: false,
                timer: 2000,
                backdrop: false,
                toast: true,
                customClass: {
                    border: '5px solid black'
                }
            })
        }
    });
}