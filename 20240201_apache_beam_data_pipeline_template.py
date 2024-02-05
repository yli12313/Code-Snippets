"""
Description: Data pipeline with Apache Beam code template. 

Date: Thu. 2/1/24
"""

# Importing the required library: beam
import apache_beam as beam

# Defining a function 'split_row()' that splits rows into a list of rows.
def split_row(element):
    return element.split(',')

# Filters records based in a condition.
def filter_records(record):
    return record[1] == ''

# Define a beam pipeline object 'p'.
p = beam.Pipeline()

# Read 'p' from some text file and apply the 'split_row()' function.
data_from_source = (
    p 
    | 'Read from text file' >> beam.io.ReadFromText('')
    | 'Split rows' >> beam.Map(split_row)
)

# Read 'data_from_source' from the operation above and filter by a certain
# condition.
filtered_data = (
    data_from_source
    | 'Filter records' >> beam.Filter(filter_records)
)

# Write the filtered data to a new text file.
filtered_data | 'Write to text file' >> beam.io.WriteToText('')

# Run the data pipeline!
p.run()
