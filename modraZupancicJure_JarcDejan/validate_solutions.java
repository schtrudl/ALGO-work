import java.io.*;
import java.util.*;

public class validate_solutions {

    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java validate_solutions <input_folder> <solutions_folder>");
            return;
        }

        File inputFile = new File(args[0]);
            File outputFile = new File(args[1]);

        try {
            validateSolution(inputFile, outputFile);
            System.out.println("VALID (OK)");
        } catch (Exception e) {
            System.out.println("ERROR -> " + e.getMessage());
        }
    }

    private static void validateSolution(File inputFile, File outputFile) throws Exception {

        //Read input data
        Scanner scIn = new Scanner(inputFile);
        scIn.useLocale(Locale.US);
        if (!scIn.hasNextInt()) throw new Exception("Empty input.");

        //Object count
        int n = scIn.nextInt();

        //Object sizes
        double[] object_sizes = new double[n + 1]; // 1-indexed
        for (int i = 1; i <= n; i++) {
            if (!scIn.hasNextDouble()) throw new Exception("Missing object sizes.");
            object_sizes[i] = scIn.nextDouble();
        }
        scIn.close();

        //Read solutions
        BufferedReader brOut = new BufferedReader(new FileReader(outputFile));

        //Read bin count
        String firstLine = brOut.readLine();
        if (firstLine == null) {
            brOut.close();
            throw new Exception("Empty solution.");
        }
        int c = Integer.parseInt(firstLine.trim());

        boolean[] used = new boolean[n + 1]; //mark used objects
        int actualBinCount = 0; //actual number of bins in the solution

        //Read individual bins
        String line;
        while ((line = brOut.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;

            actualBinCount++;

            String[] objects = line.split("\\s+");
            double binSum = 0;

            for (String object : objects) {
                int index = Integer.parseInt(object);

                //Check object index
                if (index < 1 || index > n) {
                    brOut.close();
                    throw new Exception("Invalid object index: " + index);
                }

                //Check for object duplicates
                if (used[index]) {
                    brOut.close();
                    throw new Exception("Object " + index + " is used multiple times!");
                }
                used[index] = true;
                binSum += object_sizes[index];
            }

            // Check if bin is covered (sum >= 1)
            // Use small epsilon to account for floating point accuracy
            if (binSum < 1.0 - 1e-15) {
                brOut.close();
                throw new Exception("Bin number " + actualBinCount + " is not covered (Sum: " + binSum + ")");
            }
        }
        brOut.close();

        // Check bin count
        if (c != actualBinCount) {
            throw new Exception("Reported number of bins (" + c + ") does not match the actual number (" + actualBinCount + ")");
        }
    }
}