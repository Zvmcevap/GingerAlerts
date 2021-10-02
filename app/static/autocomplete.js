let fuzzyhound = new FuzzySearch({source: search_array});

fuzzyhound.setOptions({
    score_acronym: true,
    score_test_fused: true,
    token_query_min_length: 1,
    token_field_min_length: 1
});

$('#typeahead-input').typeahead({
        minLength: 0,
        highlight: false //let FuzzySearch handle highlight
    },
    {
        name: 'search_field',
        source: fuzzyhound,
        templates: {
            suggestion: function (result) {
                return "<div>" + fuzzyhound.highlight(result) + "</div>"
            }
        }
    });

