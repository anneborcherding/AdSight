import csv
import random
from datetime import datetime, timedelta

# Provided positions and rotations
positions_rotations = [
    (50.05036212664683, 8.572061250445264, 20),
    (50.05048057710115, 8.571991151945651, 20),
    (50.05057454758693, 8.571917364051322, 20),
    (50.05091687799782, 8.572983411274532, 20),
    (50.05086259327397, 8.57257834991617, 20),
    (50.05085482034081, 8.574873504923973, 20),
    (50.05040420491223, 8.573220784650983, 20),
    (50.05044854182887, 8.573382719369938, 20),
    (50.050486920709744, 8.57357330579178, 20),
    (50.050523851302025, 8.573737954416567, 20),
    (50.05057671268854, 8.573942073602089, 20),
    (50.04981480720404, 8.571023999429775, 20),
    (50.04977519420206, 8.570869101861684, 20),
    (50.049714913487726, 8.570594175435751, 20),
    (50.04968003675224, 8.570455371121058, 20),
    (50.049626645160366, 8.570236771084828, 20),
    (50.049572822931, 8.570011465526015, 20),
    (50.04791871016219, 8.57554516134853, 155),
    (50.0480561196594, 8.574905666267387, 155),
    (50.048105081570775, 8.574765469270911, 155),
    (50.04819905670791, 8.574418666167567, 155),
    (50.048258284640994, 8.57419853228282, 155),
    (50.048296190479824, 8.573857878170669, 155),
    (50.04764388998231, 8.572367362718126, 65),
    (50.04737775515132, 8.572211178343, 65),
    (50.0471795350736, 8.572052534371835, 65),
    (50.04705317922137, 8.571944312126819, 65),
    (50.04693314085367, 8.571847158065953, 65),
]


def generate_random_data():
    people_passed = random.randint(50000, 250000)
    viewers = random.randint(5000, 25000)
    interactions = random.randint(500, 2500)
    minutes_observed = random.randint(12, 30)
    return people_passed, viewers, interactions, minutes_observed

# Generate dataset for the last 30 days
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()

# Generate a random advertiser for each billboard
advertisers = ['Advertiser_' + str(i) for i in range(1, len(positions_rotations) + 1)]
random.shuffle(advertisers)
billboard_advertisers = dict(zip(range(1, len(positions_rotations) + 1), advertisers))

with open('../data/billboard_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['date', 'billboard_name', 'latitude', 'longitude', 'rotation', 'advertiser', 'people_passed', 'viewers', 'interactions', 'minutes_observed']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    current_date = start_date
    while current_date <= end_date:
        for i, position_rotation in enumerate(positions_rotations):
            latitude, longitude, rotation = position_rotation
            people_passed, viewers, interactions, minutes_observed = generate_random_data()

            writer.writerow({
                'date': current_date.strftime('%Y-%m-%d'),
                'billboard_name': f'Billboard_{i + 1}',
                'latitude': latitude,
                'longitude': longitude,
                'rotation': rotation,
                'advertiser': billboard_advertisers[i + 1],
                'people_passed': people_passed,
                'viewers': viewers,
                'interactions': interactions,
                'minutes_observed': minutes_observed,
            })

        current_date += timedelta(days=1)

print("CSV file generated successfully.")
