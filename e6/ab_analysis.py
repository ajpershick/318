import sys
import pandas as pd
from scipy import stats as st

OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value: {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value: {more_searches_p:.3g}\n'
    '"Did more/less instructors use the search feature?" p-value: {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value: {more_instr_searches_p:.3g}'
)

def main():
    # Reading the data
    searchdata_file = sys.argv[1]
    data = pd.read_json(searchdata_file, lines=True)

    # Filtering the data
    is_even = data['uid'] % 2 == 0
    original_design = data[is_even]
    new_design = data[~is_even]
    new_design_searched = new_design[new_design['search_count'] > 0]['search_count'].size
    new_design_never_searched = new_design[new_design['search_count'] == 0]['search_count'].size
    original_design_searched = original_design[original_design['search_count'] > 0]['search_count'].size
    original_design_never_searched = original_design[original_design['search_count'] == 0]['search_count'].size

    # Testing data
    chi2, more_users_p, dof, expected = st.chi2_contingency([[new_design_searched, new_design_never_searched],
                                                         [original_design_searched, original_design_never_searched]])
    more_searches_p = st.mannwhitneyu(new_design['search_count'], original_design['search_count']).pvalue

    # Filtering instructor Data
    original_design_instructors = original_design[original_design['is_instructor'] == True]
    new_design_instructors = new_design[new_design['is_instructor'] == True]
    original_design_instructors_at_least_once = original_design_instructors[original_design_instructors['search_count'] > 0]['search_count'].size
    original_design_instructors_never_searched = original_design_instructors[original_design_instructors['search_count'] == 0]['search_count'].size
    new_design_instructors_searched = new_design_instructors[new_design_instructors['search_count'] > 0]['search_count'].size
    new_design_instructors_never_searched = new_design_instructors[new_design_instructors['search_count'] == 0]['search_count'].size

    # Testing Instructor Data
    more_instr_searches_p = st.mannwhitneyu(new_design_instructors['search_count'], original_design_instructors['search_count']).pvalue
    chi2, more_instr_p, dof, expected = st.chi2_contingency([[new_design_instructors_searched, new_design_instructors_never_searched],
                                                        [original_design_instructors_at_least_once, original_design_instructors_never_searched]])
    # Output
    print(OUTPUT_TEMPLATE.format(
        more_users_p= more_users_p,
        more_searches_p= more_searches_p,
        more_instr_p= more_instr_p,
        more_instr_searches_p= more_instr_searches_p,
    ))

if __name__ == '__main__':
    main()