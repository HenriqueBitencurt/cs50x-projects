-- Keep a log of all SQL queries you run as you solve the mystery.

-- Step 1: Check the crime scene report for July 28, 2025 on Humphrey Street
SELECT description
FROM crime_scene_reports
WHERE year = 2025 AND month = 7 AND day = 28 AND street = 'Humphrey Street';

-- Step 2: Check the interviews from witnesses on the day of the crime to get clues
SELECT name, transcript
FROM interviews
WHERE year = 2025 AND month = 7 AND day = 28;

-- Step 3: Check ATM transactions on Leggett Street on July 28, 2025 (withdrawals)
SELECT name
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_transactions.year = 2025
  AND atm_transactions.month = 7
  AND atm_transactions.day = 28
  AND atm_transactions.atm_location = 'Leggett Street'
  AND atm_transactions.transaction_type = 'withdraw';

-- Step 4: Check bakery security logs for cars exiting between 10:15 and 10:25 on July 28, 2025
SELECT name
FROM people
JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
WHERE bakery_security_logs.year = 2025
  AND bakery_security_logs.month = 7
  AND bakery_security_logs.day = 28
  AND bakery_security_logs.hour = 10
  AND bakery_security_logs.minute BETWEEN 15 AND 25
  AND bakery_security_logs.activity = 'exit';

-- Step 5: Check phone calls shorter than 60 seconds on July 28, 2025
SELECT name
FROM people
JOIN phone_calls ON people.phone_number = phone_calls.caller
WHERE phone_calls.year = 2025
  AND phone_calls.month = 7
  AND phone_calls.day = 28
  AND phone_calls.duration < 60;

-- Step 6: Find the earliest flight out of Fiftyville on July 29, 2025
SELECT flights.id, destination_airport_id, hour, minute
FROM flights
JOIN airports ON flights.destination_airport_id = airports.id
WHERE year = 2025 AND month = 7 AND day = 29
ORDER BY hour ASC, minute ASC LIMIT 1;

-- Step 7: Check the destination city for that flight
SELECT city
FROM airports
WHERE id = '(destination_airport_id_found)';

-- Step 8: Check the passengers on that flight to confirm who boarded and find the accomplice
SELECT name
FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE passengers.flight_id = (flight_id_found);

-- Step 9: Check who Bruce called right after the theft to identify the accomplice
SELECT name
FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE phone_calls.year = 2025
  AND phone_calls.month = 7
  AND phone_calls.day = 28
  AND phone_calls.duration < 60
  AND phone_calls.caller = (SELECT phone_number FROM people WHERE name = 'Bruce');

