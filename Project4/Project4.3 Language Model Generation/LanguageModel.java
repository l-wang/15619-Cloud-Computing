import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.HTable;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.hbase.mapreduce.TableReducer;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class LanguageModel {

	public static class TheMap extends Mapper<LongWritable, Text, Text, Text> {
        private Text output_prefix = new Text();

        private Text output_after = new Text();

        private int times_min = 2;


        @Override
        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
        	
            // the input string.
            String line_string = value.toString();

            // split the input string to 2.
            String[] string_group = line_string.split("\t");

            // get the whole word.
            String word_whole = string_group[0];

            // get the times that the whole word exit.
            int times = Integer.parseInt(string_group[1]);

            // filter the words which only exit less than 2 times.
            if (times < times_min) {
                return;
            }

            // split the word_whold into small words.
            String[] string_group_t = word_whole.split(" ");

            // if there is only one word like 'a', just skip it.
            if (string_group_t.length <= 1) {
                return;
            }

            // find the position of last_word " "
            int endIndex = word_whole.lastIndexOf(" ");

            String line_prefix = line_string.substring(0, endIndex).trim();		// prefix

            String last_word = word_whole.substring(endIndex).trim();	

            last_word += " " + times;

            output_prefix.set(line_prefix);
            output_after.set(last_word);

            context.write(output_prefix, output_after);
        }
    }

	public static class Reduce extends TableReducer<Text, Text, ImmutableBytesWritable> {

        // get the number of words that display in the website.
        private int N_FirstRank = 5;

        private Configuration config = HBaseConfiguration.create();
        
        public static final byte[] FAMILY_COL = Bytes.toBytes("i");
		public static final byte[] COL = Bytes.toBytes("a");

        @Override
        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            String last_word = "";
            int number, sum_number = 0;

            // creat a map to sort.
            Map <String, Integer> map_list = new HashMap<String, Integer>();
            int total_size = 0;
            String wordnext = "";
            double wordcount = 0;
            double Probability = 0;

            for (Text value : values) {
                String value_string = value.toString();
                String count = "";

                // find the position of the " "
                int endIndex = value_string.lastIndexOf(" ");

                last_word = value_string.substring(0, endIndex);

                count = value_string.substring(endIndex).trim();
                number = Integer.parseInt(count);

                map_list.put(last_word, number);
                sum_number += number;
            }

            List<Map.Entry<String, Integer>> ListSort = new ArrayList<Map.Entry<String, Integer>> (map_list.entrySet());

            // sort the result.
            Collections.sort(ListSort,
                new Comparator <Map.Entry<String, Integer>>() {
                    public int compare(Map.Entry < String, Integer > o1,
                        Map.Entry < String, Integer > o2) {
                        int result = (Integer) o2.getValue() - (Integer) o1.getValue();
                        return result;
                    }
                });

            // get the size of the result which output.
            if (ListSort.size() > N_FirstRank) {
                total_size = N_FirstRank;
            } else {
                total_size = ListSort.size();
            }

            Put put = new Put(Bytes.toBytes(key.toString()));

            int i = 0;

            while (i < total_size) {
                wordnext = ListSort.get(i).getKey();
                wordcount = ListSort.get(i).getValue();
                Probability = wordcount * 100.0 / sum_number;
                String mix = wordnext + "-" + wordcount;
                put.add(Bytes.toBytes("Probability"),
        	            Bytes.toBytes(wordnext),
        	            Bytes.toBytes("" + Probability));
                i++;
            }

            if(!put.isEmpty()) {
            	context.write(new ImmutableBytesWritable(key.getBytes()), put);
            }
            
        }

    }

    
    
    public static void main(String[] args) throws Exception {
    	
    	Configuration conf = HBaseConfiguration.create();
		Job job = new Job(conf, "model");
		job.setJarByClass(LanguageModel.class);

		TableMapReduceUtil.initTableReducerJob("model", // output table
				Reduce.class, // reducer class
				job);

		job.setNumReduceTasks(10);

		job.setMapperClass(TheMap.class);
		job.setReducerClass(Reduce.class);

		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
//		job.setInputFormatClass(TextInputFormat.class);

		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		 
		// get the parameters.
		conf.set("Times_Min", args[2]);
		conf.set("N_FirstRank", args[3]);

		System.exit(job.waitForCompletion(true) ? 0 : 1);
    	
    	
    	
    	
    }
}