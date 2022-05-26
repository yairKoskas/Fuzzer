def get_value_percentage(coverage_data, new_coverage_data):
    new_blocks = set(new_coverage_data) - set(coverage_data)
    # once integration bugs are solved, it'll be easier to manipulate the coverage data
    # to conform to known formulas calculating value of new coverage
    return (len(new_blocks) / len(new_coverage_data)) * 100