{#
    This macro returns the description from payment_type column
#}
{% macro get_yellow_payment_type_description(payment_type) -%}
    case cast({{payment_type}} as integer)
        when 0 then 'Flex Fare trip'
        when 1 then 'Credit card'
        when 2 then 'Cash'
        when 3 then 'No charge'
        when 4 then 'Dispute'
        when 5 then 'Unknown'
        when 6 then 'Voided trip'
        else 'EMPTY'
    end
{%- endmacro %}

{#
    This macro returns the decription from vendorid column
#}
{% macro get_vendorid_description(vendorid) -%}
    case cast({{vendorid}} as integer)
        when 1 then 'Creative Mobile Technologies, LLC'
        when 2 then 'Curb Mobility, LLC'
        when 6 then 'Myle Technologies Inc'
        when 7 then 'Helix'
        else 'EMPTY'
    end
{%- endmacro %}