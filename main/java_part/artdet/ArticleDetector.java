/*
 * ArticleDetector.java
 * 
 * Code for final project in 11-761, CMU, Spring 2013
 * Weston Feely, Mario Piergallini, Callie Vaughn, Thomas VanDrunen
 */

package artdet;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.Random;
import java.util.StringTokenizer;

import weka.classifiers.Classifier;
import weka.classifiers.bayes.NaiveBayesSimple;
import weka.classifiers.xml.XMLClassifier;
import weka.core.Instances;
import weka.core.Instance;
import weka.core.converters.ConverterUtils;
import weka.classifiers.functions.LibLINEAR;
import weka.classifiers.functions.Logistic;

/**
 * Program to determine whether a news article is real or fake,
 * given a Weka classifier.
 * 
 * Note about runtime error message: when you run this, you'll get the
 * following error/warning message:
 * 
 * ---Registering Weka Editors---
 * Trying to add database driver (JDBC): RmiJdbc.RJDriver - Error, not in CLASSPATH?
 * Trying to add database driver (JDBC): jdbc.idbDriver - Error, not in CLASSPATH?
 * Trying to add database driver (JDBC): org.gjt.mm.mysql.Driver - Error, not in CLASSPATH?
 * Trying to add database driver (JDBC): com.mckoi.JDBCDriver - Error, not in CLASSPATH?
 * Trying to add database driver (JDBC): org.hsqldb.jdbcDriver - Error, not in CLASSPATH?
 * 
 * According to http://weka.wikispaces.com/Trying+to+add+JDBC+driver...+-+Error,+not+in+CLASSPATH%3F
 * we can just ignore this.
 * 
 * @author Thomas Vandrunen
 */

public class ArticleDetector {

	/**
	 * Main method
	 * @param args - See usage() for explanation
	 */
	public static void main(String[] args) {
	
		try { // throwing all Weka exceptions and File I/O exceptions to a single catch

			// boundary between real and fake articles (with dummy default value)
			double threshold = .5;  
			
			// do real articles rank above the threshold?
			boolean high = true;  
			
			// file containing feature vectors for articles to classify
			String vectorFile = null;  
			
			// file containing pre-trained model (if applicable)
			String modelFile = null;
			
			// the classifier for articles
			Classifier clsfier = null;
			
			// file for training data (if applicable; with dummy default value)
			String trainingFile = "J48 PointwisePredictions.csv";
			
			try {   // read flags (see usage())
					// (note the i++ for flags that take a value)
				for (int i = 0; i < args.length; i++) {
					String item = args[i];
					if (item.equals("-t")) 
						trainingFile = args[++i];
					else if (item.equals("-l"))
						modelFile = args[++i];
					else if (item.equals("-th"))
						threshold = Double.parseDouble(args[++i]);
					else if (item.equals("-high"))
						high = true;
					else if (item.equals("-low"))
						high = false;
					else if (item.equals("-mockup"))
						clsfier = new GoofyClassifier();
					else // if it's not one of the above flags, assume it's 
						// the file with feature vectors for articles
						vectorFile = item;
				}
			} catch(ArrayIndexOutOfBoundsException aioobe) {
				usage();
			}

			if (vectorFile == null) {
				System.out.println("Missing vector file");
				usage();
			}
			
			// if a file for a previously trained model is given,
			// load it
			if (modelFile != null) 
				clsfier = (Classifier) (new XMLClassifier()).read(modelFile);			
			// otherwise, train one using data in the training file
			else if (clsfier == null) {
				clsfier = new Logistic();
				
				ConverterUtils.DataSource source = new ConverterUtils.DataSource(trainingFile);
				Instances trainingData = source.getDataSet();

				// assume class index is 0!!!!
				trainingData.setClassIndex(0);
				clsfier.buildClassifier(trainingData);
			}

			// -- iterate over the feature vectors in the file ---
			
			// the following is obscelete if we use weka's own tools
			// for reading in data
			// -------
			//int i = 0;  // counter so we can indicate which article we're on

			// see documentation for getTestInstances() to understand
			// how we're iterating over vectors
			/*
			for (Instance currentArticle : 
				getTestInstances(new FileReader(vectorFile))) {

				// ************
				// Right now, Weka rejects this with
				// 		"Exception: Instance doesn't have access to a dataset!"
				// ************
				double result = clsfier.classifyInstance(currentArticle);
				
				// Determine real or fake based on comparison with threshold
				System.out.println(i++ + ": " + result + " \t " +
						((result > threshold) == high ? "Real" : "Fake"));	

			}
			*/
			// ------------
			
			ConverterUtils.DataSource testSource = new ConverterUtils.DataSource(vectorFile);
			Instances testData = testSource.getDataSet();
			testData.setClassIndex(0);
			for (int i = 0; i < testData.numInstances(); i++) {
				double result = clsfier.classifyInstance(testData.instance(i));
			
				// Determine real or fake based on comparison with threshold
				System.out.println((1-result) + "\t " + result + "\t" +
						((result > threshold) == high ? "1" : "0"));	

			}
			
		
		} catch (Exception e) {
			System.out.println("Exception: " + e.getMessage());
			System.exit(-1);
		}
	
	}

	/**
	 * Display usage information 
	 */
	private static void usage() {
		System.out.println("java artdec.ArticleDetector [options] vectorFile\n" +
				"where options are\n" +
				"\t-t trainingFile : trains a classifier from data in trainingFile\n" +
				"\t-l xmlFile : loads previously trained classifier from xmlFile\n" +
				"\t\t(If both -t and -l are used, -l overrides -t;\n" +
				"\t\t if neither are given, default is to train NaiveBayes on cpu.arff)\n" +
				"\t-th num : sets real/fake threshold to num (default .5)\n" +
				"\t-high : articles classed above threshold are real (default)\n" +
				"\t-low : articles classed below threshold are real\n");
		System.exit(0);
		
	}
	

	// right now this is not being used... I'm assuming the file
	// with feature vectors can be read by Weka's classes
	/**
	 * Package the feature vectors in a way that can be used with
	 * a Java extended for loop. This is a great example of what stinks
	 * about Java. This is an I-wish-I-were-programming-in-Python moment.
	 * @param vectors A Reader which gives vector descriptions one line at a time
	 * @return An iterable that produces an iterator for Weka instances
	 */
	private static Iterable<Instance> getTestInstances(Reader vectors) {
		// To read line line at a time, we need to wrap the vectors reader
		// into a buffered reader. To use a local variable inside an
		// inner class, we need to declare it final
		final BufferedReader buffy = new BufferedReader(vectors);

		// Java stinks because to use a slick extended for loop we 
		// need an *Iterable*, not an *Iterator*. Thus we can't just return
		// an iterator, but we need to package that iterator up into
		// a dummy iterable that does nothing but return that iterator
		return new Iterable<Instance>() {
				public Iterator<Instance> iterator() {

					return new Iterator<Instance>() {
						/**
						 * Is there another vector? Yes, if there are more
						 * lines in the file
						 */
						public boolean hasNext() {
							try {
								return buffy.ready();
							} catch (IOException ioe) {
								System.out.println("Exception: " + ioe.getMessage());
								System.exit(-1);
							}
							return false; // shouldn't be necessary, but javac's
								// cfg analysis can't tell that
								// (CFG here stands for "control flow graph", not
								// "context free grammar")
						}

						/**
						 * Get the next feature vector as a Weka instance. We read
						 * in the next line of the file, which should contain a sequence
						 * of floats. Package them up in an array and use that
						 * to make a new Instance
						 */
						public Instance next() {

							// collection of feature values for the current article
							ArrayList<Double> vals = new ArrayList<Double>();
							try {
								// chop up the next line into doubles, adding them to vals
								for (StringTokenizer tokey = 
										new StringTokenizer(buffy.readLine());
										tokey.hasMoreElements(); )
									vals.add(Double.parseDouble(tokey.nextToken()));
							} catch(IOException ioe) {
								System.out.println("Exception: " + ioe.getMessage());
								System.exit(-1);
							}

							// Java stinks because there is no simple way turn an
							// ArrayList of Double wrappers into an array of double
							// primitives, making us stoop to this rigmarole
							double[] primVals = new double[vals.size()];
							int i = 0;
							for (double v : vals) primVals[i++] = v;
							
							// ************
							// Since I don't know Weka, I imagine we really need to do
							// more with this instance to make it usable
							// *************
							return new Instance(0, primVals);
						}

						public void remove() {
							throw new UnsupportedOperationException();
						}
					};
				}
				
				
			};
		
	}
	
	// I made this pseudo-classifier that acts randomly so I could
	// test the rest of the program before I got help
	// from someone who understood Weka
	private static class GoofyClassifier extends Classifier {

		private Random randy = new Random();
		
		@Override
		public void buildClassifier(Instances arg0) throws Exception {
			// do nothing
		}
		
		@Override
		public double classifyInstance(Instance instance) {
			return randy.nextDouble();
		}
		
	}
	
}
