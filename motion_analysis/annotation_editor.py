import collections
import numpy as np


class AnnotationEditor(object):
    def __init__(self):
        self._semantic_annotation = collections.OrderedDict()
        self._label_color_map = collections.OrderedDict()
        self.prev_annotation_edit_frame_idx = 0

    def clear_timeline(self, label):
        if label in self._semantic_annotation:
            self._semantic_annotation[label] = []
            return True
        else:
            return False
    
    def set_annotation_edit_start(self, frame_idx):
        self.prev_annotation_edit_frame_idx = frame_idx

    def set_annotation(self, annotation, color_map):
        self._semantic_annotation = annotation
        self._label_color_map = color_map

    def add_label(self, label, color):
        if label not in self._semantic_annotation:
            self._semantic_annotation[label] = []
            self._label_color_map[label] = color

    def remove_label(self, label):
        if label in self._semantic_annotation:
            del self._semantic_annotation[label]

    def clean_annotation_sections(self):
        """ order sections remove empty sections and merge neighboring sections"""
        annotations = self._semantic_annotation
        for label in  annotations:
            n_sections_before = len(annotations[label])
            new_sections = []
            for i, indices in enumerate(annotations[label]):
                if len(indices) > 0:
                    new_sections.append(indices)
                else:
                    print("delete section", i)
            new_sections.sort(key=lambda x : x[0]) # order sections
            n_new_sections = len(new_sections)
            merged_new_sections = []
            merged_idx = -1
            for i in range(0, n_new_sections):
                if i == merged_idx:
                    continue
                if i+1 < n_new_sections and (new_sections[i+1][0] -1 in new_sections[i] or new_sections[i+1][0] in new_sections): # merge right
                    merged_idx = i+1
                    merged_new_sections.append(new_sections[i]+new_sections[i+1])
                    print("merged sections", i, i+1)
                else:
                    merged_new_sections.append(new_sections[i])
            annotations[label] = merged_new_sections
            print("before merge:",n_sections_before,"after merge:", len(merged_new_sections))
        self._semantic_annotation = annotations

    def create_annotation_section(self, frame_idx, label):
        n_labels = len(self._semantic_annotation)
        if label in self._semantic_annotation:
            if self.prev_annotation_edit_frame_idx < frame_idx:
                section = list(range(self.prev_annotation_edit_frame_idx, frame_idx))
            else:
                section = list(range(frame_idx, self.prev_annotation_edit_frame_idx))
            self._semantic_annotation[label] += [section]
            self.prev_annotation_edit_frame_idx = frame_idx
            print("set annotation", self.prev_annotation_edit_frame_idx, frame_idx)
            self.clean_annotation_sections()
            return True
        else:
            print("no label found")
            return False

    def remove_annotation_section(self, frame_idx, current_label):
        labels = list(self._semantic_annotation.keys())
        print("try to remove annoation at", frame_idx, len(labels))
        if len(labels) > 0:
            current_entry_idx = self.get_section_of_current_frame(current_label, frame_idx)
            if current_entry_idx is None:
                print("did not find section at", frame_idx)
                return
            old_list = self._semantic_annotation[current_label][current_entry_idx]
            if self.prev_annotation_edit_frame_idx < frame_idx:
                min_v = self.prev_annotation_edit_frame_idx
                max_v = frame_idx
            else:
                min_v = frame_idx
                max_v = self.prev_annotation_edit_frame_idx
            new_list = []
            for v in old_list:
                if v < min_v or v >= max_v:
                    new_list.append(v)
            print("remove annotation", len(old_list),len(new_list), min_v, max_v)
            self._semantic_annotation[current_label][current_entry_idx] = new_list
            self.clean_annotation_sections()
            return True
        else:
            return False
       
    def get_next_closest_label_entry(self, frame_idx, label, entry):
        indices = self._semantic_annotation[label][entry]
        indices.sort()
        if abs(frame_idx -indices[0]) < abs(frame_idx - indices[-1]):
            return self.get_prev_label_entry(label, entry)
        else:
            return self.get_next_label_entry(label, entry)

    def overwrite_current_section_by_neighbor(self, frame_idx):
        if len(self._semantic_annotation) > 1:
            current_label, current_entry_idx = self.get_annotation_of_frame(frame_idx)
            next_closest_label, next_closest_entry_idx = self.get_next_closest_label_entry(frame_idx, current_label, current_entry_idx)
            self.overwrite_section(next_closest_label, next_closest_entry_idx, current_label, current_entry_idx, frame_idx)
            self.clean_annotation_sections()
            return True
        else:
            return False

    def get_annotation_of_frame(self, frame_idx, ignore_label=None):
        labels = list(self._semantic_annotation.keys())
        current_label = labels[0]
        delta = np.inf
        current_entry_idx = None
        for label in labels:
            if label == ignore_label:
                continue
            entry_idx = 0
            for entry in self._semantic_annotation[label]:
                for idx in entry:
                    if abs(idx - frame_idx) < delta:
                        delta = abs(idx - frame_idx)
                        current_label = label
                        current_entry_idx = entry_idx
                        if delta == 0:
                            break
                entry_idx+=1
        return current_label, current_entry_idx

    def get_next_label_entry(self, label, entry):
        indices = self._semantic_annotation[label][entry]
        indices.sort()
        return self.get_annotation_of_frame(indices[-1], ignore_label=label)

    def get_prev_label_entry(self, label, entry):
        indices = self._semantic_annotation[label][entry]
        indices.sort()
        return self.get_annotation_of_frame(indices[0], ignore_label=label)   

    def split_annotation(self, frame_idx, n_frames):
        labels = list(self._semantic_annotation)
        n_labels = len(labels)
        if n_labels > 0:
            current_label, current_entry_idx = self.get_annotation_of_frame(frame_idx)
            self.split_annotation_section(current_label, frame_idx)
        else:
            section1_label ="c" + str(n_labels)
            section2_label = "c" + str(n_labels + 1)
            self._semantic_annotation[section1_label] = [list(range(0, frame_idx))]
            self._label_color_map[section1_label] = [0,0,0]
            self._semantic_annotation[section2_label] = [list(range(frame_idx, n_frames))]
            self._label_color_map[section2_label] = [0,0,0]
    
    def split_annotation_section(self, current_label, frame_idx):
        entries = self._semantic_annotation[current_label]
        entry_idx = self.get_section_of_current_frame(current_label, frame_idx)
        print("split", current_label, entry_idx)
        if entry_idx is None:
            return
        if entry_idx < 0 or entry_idx > len(entries):
            return
        idx_list = entries[entry_idx]
        idx_list.sort()
        start_idx = idx_list[0]
        end_idx = idx_list[-1]
        section_a = list(range(start_idx, frame_idx))
        section_b = list(range(frame_idx, end_idx))
        #replace the old section
        self._semantic_annotation[current_label][entry_idx] = section_a
        # create a new entry
        new_label = current_label + "_split"
        self._semantic_annotation[new_label]= [section_b]
        #copy color
        self._label_color_map[new_label] = self._label_color_map[current_label]
        
    def merge_annotation(self, frame_idx):
        if len(self._semantic_annotation) > 1:
            current_label, current_entry_idx = self.get_annotation_of_frame(frame_idx)
            next_closest_label, next_entry_idx = self.get_next_closest_label_entry(frame_idx, current_label, current_entry_idx)
            self.merge_annotation_sections(current_label, next_closest_label, next_entry_idx)
            return True
        else:
            return False

    def merge_annotation_sections(self, label_a, label_b, b_entry_idx):
        print("merge", label_a, "and", label_b)
        indices = self._semantic_annotation[label_b][b_entry_idx]
        self._semantic_annotation[label_a].append(indices)
        new_indices_list = []
        for idx, frame_indices in enumerate(self._semantic_annotation[label_b]):
            if idx != b_entry_idx:
                new_indices_list.append(frame_indices)
        if len(new_indices_list) > 0:
            self._semantic_annotation[label_b] = new_indices_list
        else:
            del self._semantic_annotation[label_b]
            del self._label_color_map[label_b]

    def overwrite_section(self, next_label, next_entry, cur_label, cur_entry, frame_idx):
        """ overwrite current section with closest section """
        print("change", next_label,next_entry, "to", cur_label,cur_entry )
        annotations = self._semantic_annotation
        next_idx_list = annotations[next_label][next_entry]
        cur_idx_list = annotations[cur_label][cur_entry]
        new_cur_idx_list = cur_idx_list
        new_next_idx_list = next_idx_list
        
        if next_idx_list[0] >= frame_idx and frame_idx <= cur_idx_list[-1]: # next is right to cur_label
            next_start_idx = next_idx_list[0]
            next_end_idx = next_idx_list[-1]
            cur_start_idx = cur_idx_list[0]
            cur_end_idx = cur_idx_list[-1]
            new_next_idx_list += list(range(frame_idx, cur_end_idx+1))
            new_cur_idx_list = list(range(cur_start_idx, frame_idx))
            annotations[next_label][next_entry] = new_next_idx_list
            annotations[cur_label][cur_entry] = new_cur_idx_list
            print("next is right")
        elif  next_idx_list[0] <= frame_idx and  frame_idx  <= cur_idx_list[-1] : # next is left to cur_label
            next_end_idx = next_idx_list[-1]
            cur_end_idx = cur_idx_list[-1]
            new_next_idx_list += list(range(next_end_idx, frame_idx))
            new_cur_idx_list = list(range(frame_idx, cur_end_idx+1))
            print("next is left")
            annotations[next_label][next_entry] = new_next_idx_list
            annotations[cur_label][cur_entry] = new_cur_idx_list
        self._semantic_annotation = annotations

    def get_section_of_current_frame(self, label, frame_idx):
        delta = np.inf
        current_entry_idx = None
        entry_idx = 0
        for entry in self._semantic_annotation[label]:
            for idx in entry:
                if abs(idx - frame_idx) < delta:
                    delta = abs(idx - frame_idx)
                    current_entry_idx = entry_idx
                    if delta == 0:
                        break
            entry_idx+=1
        return current_entry_idx
